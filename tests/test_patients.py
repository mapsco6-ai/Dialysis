import pytest
from rest_framework import status

from apps.core.roles import Roles

pytestmark = pytest.mark.django_db


def test_doctor_creates_patient_and_mrn_is_auto_generated(auth_client):
    client, _ = auth_client(Roles.DOCTOR)
    response = client.post(
        "/api/patients/",
        {
            "first_name": "Ahmed",
            "father_name": "Ali",
            "family_name": "Hassan",
            "date_of_birth": "1980-01-01",
            "gender": "M",
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["mrn"] == "MRN000001"

    second = client.post(
        "/api/patients/",
        {
            "first_name": "Sara",
            "date_of_birth": "1990-01-01",
            "gender": "F",
        },
        format="json",
    )
    assert second.data["mrn"] == "MRN000002"


def test_receptionist_sees_basic_serializer_without_clinical_fields(auth_client, patient):
    client, _ = auth_client(Roles.RECEPTIONIST)
    response = client.get(f"/api/patients/{patient.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert "blood_type" not in response.data
    assert "medical_history" not in response.data


def test_doctor_sees_full_serializer_with_clinical_fields(auth_client, patient):
    client, _ = auth_client(Roles.DOCTOR)
    response = client.get(f"/api/patients/{patient.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert "blood_type" in response.data
    assert "medical_history" in response.data


def test_warehouse_keeper_cannot_write_patients(auth_client):
    client, _ = auth_client(Roles.WAREHOUSE_KEEPER)
    response = client.post(
        "/api/patients/",
        {"first_name": "X", "date_of_birth": "1990-01-01", "gender": "M"},
        format="json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patient_history_is_tracked(patient):
    assert patient.history.count() == 1
    patient.first_name = "Updated"
    patient.save()
    assert patient.history.count() == 2
