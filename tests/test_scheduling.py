from datetime import time

import pytest
from rest_framework import status

from apps.core.roles import Roles
from apps.scheduling.models import DialysisSchedule, Machine, Shift

pytestmark = pytest.mark.django_db


@pytest.fixture
def shift(db):
    return Shift.objects.create(name="Morning", start_time=time(6, 0), end_time=time(10, 0))


@pytest.fixture
def machines(db):
    return [Machine.objects.create(code=f"M-{i}") for i in range(1, 4)]


@pytest.fixture
def schedule(db, patient, shift):
    return DialysisSchedule.objects.create(
        patient=patient,
        days_of_week=[0, 2, 5],
        start_date="2026-01-01",
        preferred_shift=shift,
    )


def test_receptionist_checks_in_patient_with_dynamic_machine_assignment(
    auth_client, schedule, shift, machines
):
    client, _ = auth_client(Roles.RECEPTIONIST)
    response = client.post(f"/api/dialysis-schedules/{schedule.id}/check-in/")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["machine"] is not None
    assert response.data["status"] == "checked_in"


def test_check_in_does_not_double_book_a_machine(auth_client, schedule, shift, machines):
    client, _ = auth_client(Roles.RECEPTIONIST, username="recept_dblbook")
    first = client.post(f"/api/dialysis-schedules/{schedule.id}/check-in/")

    from apps.patients.models import Patient

    other_patient = Patient.objects.create(
        first_name="Other", date_of_birth="1988-01-01", gender="M"
    )
    from apps.scheduling.models import DialysisSchedule as DS

    other_schedule = DS.objects.create(
        patient=other_patient,
        days_of_week=[0],
        start_date="2026-01-01",
        preferred_shift=shift,
    )
    second = client.post(f"/api/dialysis-schedules/{other_schedule.id}/check-in/")

    assert first.data["machine"] != second.data["machine"]


def test_doctor_cannot_check_in_patient(auth_client, schedule, shift, machines):
    client, _ = auth_client(Roles.DOCTOR)
    response = client.post(f"/api/dialysis-schedules/{schedule.id}/check-in/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_check_in_fails_when_no_machine_available(auth_client, schedule, shift):
    client, _ = auth_client(Roles.RECEPTIONIST)
    response = client.post(f"/api/dialysis-schedules/{schedule.id}/check-in/")
    assert response.status_code == status.HTTP_409_CONFLICT
