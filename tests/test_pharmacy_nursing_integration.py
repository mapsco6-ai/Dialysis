"""End-to-end integration coverage for the two cross-app flows the
architecture is built around: doctor prescribes -> pharmacy restocks from
the warehouse -> dispense, and doctor prescribes -> nurse gets a MAR task.
"""

import pytest
from rest_framework import status

from apps.core.roles import Roles
from apps.nursing.models import MedicationAdministrationRecord
from apps.pharmacy.models import Drug, DrugStock
from apps.warehouse.models import SupplyItem, SupplyStock

pytestmark = pytest.mark.django_db


@pytest.fixture
def warehouse_item(db):
    item = SupplyItem.objects.create(
        name="Heparin bulk", category="medication_bulk", unit_of_measure="vial"
    )
    SupplyStock.objects.create(supply_item=item, quantity_on_hand=50)
    return item


@pytest.fixture
def drug(db, warehouse_item):
    return Drug.objects.create(name="Heparin", form="injection", warehouse_item=warehouse_item)


def test_prescription_immediately_creates_a_mar_task(auth_client, patient, drug):
    doctor_client, doctor = auth_client(Roles.DOCTOR, username="doc_presc")
    response = doctor_client.post(
        "/api/prescriptions/",
        {
            "patient": str(patient.id),
            "drug": str(drug.id),
            "dosage": "5000 IU",
            "frequency": "before session",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED

    mar_entries = MedicationAdministrationRecord.objects.filter(prescription_id=response.data["id"])
    assert mar_entries.count() == 1
    assert mar_entries.first().status == MedicationAdministrationRecord.Status.PENDING


def test_nurse_administers_generated_mar_task(auth_client, patient, drug):
    doctor_client, _ = auth_client(Roles.DOCTOR, username="doc_administer")
    presc = doctor_client.post(
        "/api/prescriptions/",
        {
            "patient": str(patient.id),
            "drug": str(drug.id),
            "dosage": "5000 IU",
            "frequency": "before session",
        },
        format="json",
    ).data
    mar = MedicationAdministrationRecord.objects.get(prescription_id=presc["id"])

    nurse_client, nurse = auth_client(Roles.NURSE, username="nurse_administer")
    response = nurse_client.post(
        f"/api/mar/{mar.id}/administer/", {"dose_given": "5000 IU"}, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    mar.refresh_from_db()
    assert mar.status == MedicationAdministrationRecord.Status.GIVEN
    assert mar.administered_by == nurse


def test_full_pharmacy_restock_flow(auth_client, drug, warehouse_item, patient):
    pharmacist_client, pharmacist = auth_client(Roles.PHARMACIST, username="pharm_flow")
    warehouse_client, warehouse_keeper = auth_client(Roles.WAREHOUSE_KEEPER, username="wh_flow")
    doctor_client, _ = auth_client(Roles.DOCTOR, username="doc_flow")

    assert drug.quantity_on_hand == 0

    request_response = pharmacist_client.post(
        "/api/pharmacy-stock-requests/",
        {"drug": str(drug.id), "quantity_requested": 20},
        format="json",
    )
    assert request_response.status_code == status.HTTP_201_CREATED
    request_id = request_response.data["id"]

    self_approve = pharmacist_client.post(f"/api/pharmacy-stock-requests/{request_id}/approve/")
    assert self_approve.status_code == status.HTTP_403_FORBIDDEN

    approve = warehouse_client.post(f"/api/pharmacy-stock-requests/{request_id}/approve/")
    assert approve.status_code == status.HTTP_200_OK
    assert approve.data["status"] == "fulfilled"

    warehouse_item.refresh_from_db()
    assert warehouse_item.quantity_on_hand == 30

    drug.refresh_from_db()
    assert drug.quantity_on_hand == 20

    prescription = doctor_client.post(
        "/api/prescriptions/",
        {
            "patient": str(patient.id),
            "drug": str(drug.id),
            "dosage": "2000 IU",
            "frequency": "weekly",
        },
        format="json",
    ).data

    batch = DrugStock.objects.get(drug=drug)
    dispense = pharmacist_client.post(
        "/api/dispense-records/",
        {
            "prescription": prescription["id"],
            "drug_stock": str(batch.id),
            "quantity_dispensed": 5,
        },
        format="json",
    )
    assert dispense.status_code == status.HTTP_201_CREATED
    batch.refresh_from_db()
    assert batch.quantity_on_hand == 15


def test_approve_rejects_when_warehouse_stock_insufficient(auth_client, drug, warehouse_item):
    pharmacist_client, _ = auth_client(Roles.PHARMACIST, username="pharm_insufficient")
    warehouse_client, _ = auth_client(Roles.WAREHOUSE_KEEPER, username="wh_insufficient")

    request_response = pharmacist_client.post(
        "/api/pharmacy-stock-requests/",
        {"drug": str(drug.id), "quantity_requested": 999},
        format="json",
    )
    request_id = request_response.data["id"]

    approve = warehouse_client.post(f"/api/pharmacy-stock-requests/{request_id}/approve/")
    assert approve.status_code == status.HTTP_409_CONFLICT
