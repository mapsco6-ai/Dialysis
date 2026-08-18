import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.core.roles import Roles
from apps.patients.models import Patient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def make_user(db):
    def _make(username, role=None, **kwargs):
        user = User.objects.create_user(
            username=username, password="testpass123", full_name=username, **kwargs
        )
        if role:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        return user

    return _make


@pytest.fixture
def auth_client(api_client, make_user):
    """Returns a callable: role -> authenticated APIClient for a fresh user
    of that role. Uses force_authenticate so tests exercise the DRF
    permission classes directly, without needing a real JWT round trip
    (that flow is covered separately in test_auth.py)."""

    def _auth(role, username=None, **kwargs):
        user = make_user(username or f"user_{role}", role, **kwargs)
        client = APIClient()
        client.force_authenticate(user=user)
        return client, user

    return _auth


@pytest.fixture
def doctor_user(make_user):
    return make_user("doctor1", Roles.DOCTOR)


@pytest.fixture
def patient(db, doctor_user):
    return Patient.objects.create(
        first_name="Test",
        family_name="Patient",
        date_of_birth="1980-01-01",
        gender="M",
        created_by=doctor_user,
    )
