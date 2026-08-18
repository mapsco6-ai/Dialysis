import pytest
from rest_framework import status

from apps.core.roles import Roles
from apps.lab.models import LabOrder, LabTestType

pytestmark = pytest.mark.django_db


@pytest.fixture
def test_type(db):
    return LabTestType.objects.create(name="Serum Creatinine", code="CREA", unit="mg/dL")


def test_doctor_orders_lab_tech_enters_result_manually(auth_client, patient, test_type):
    doctor_client, _ = auth_client(Roles.DOCTOR, username="doc_lab")
    lab_client, lab_tech = auth_client(Roles.LAB_TECH, username="lab_tech1")

    order_response = doctor_client.post(
        "/api/lab-orders/",
        {"patient": str(patient.id), "test_type": str(test_type.id)},
        format="json",
    )
    assert order_response.status_code == status.HTTP_201_CREATED
    assert order_response.data["status"] == "ordered"
    order_id = order_response.data["id"]

    result_response = lab_client.post(
        "/api/lab-results/",
        {"lab_order": order_id, "result_value": "1.1", "unit": "mg/dL"},
        format="json",
    )
    assert result_response.status_code == status.HTTP_201_CREATED
    assert result_response.data["source"] == "manual"

    order = LabOrder.objects.get(id=order_id)
    assert order.status == LabOrder.Status.RESULTED


def test_doctor_cannot_enter_lab_result_directly(auth_client, patient, test_type):
    doctor_client, _ = auth_client(Roles.DOCTOR, username="doc_lab2")
    order_id = doctor_client.post(
        "/api/lab-orders/",
        {"patient": str(patient.id), "test_type": str(test_type.id)},
        format="json",
    ).data["id"]

    response = doctor_client.post(
        "/api/lab-results/",
        {"lab_order": order_id, "result_value": "1.1"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_pharmacist_has_no_lab_access(auth_client):
    client, _ = auth_client(Roles.PHARMACIST, username="pharm_lab")
    response = client.get("/api/lab-orders/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
