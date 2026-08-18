import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.core.roles import Roles

pytestmark = pytest.mark.django_db


def test_login_returns_access_and_refresh_tokens(make_user):
    make_user("doctor1", Roles.DOCTOR)
    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {"username": "doctor1", "password": "testpass123"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


def test_login_rejects_wrong_password(make_user):
    make_user("doctor1", Roles.DOCTOR)
    client = APIClient()

    response = client.post(
        "/api/auth/login/",
        {"username": "doctor1", "password": "wrong"},
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_token_carries_role_claim(make_user):
    make_user("doctor1", Roles.DOCTOR)
    client = APIClient()
    response = client.post(
        "/api/auth/login/",
        {"username": "doctor1", "password": "testpass123"},
        format="json",
    )

    import jwt

    payload = jwt.decode(response.data["access"], options={"verify_signature": False})
    assert payload["roles"] == [Roles.DOCTOR]


def test_me_endpoint_requires_authentication():
    client = APIClient()
    response = client.get("/api/auth/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_endpoint_returns_current_user(make_user):
    make_user("doctor1", Roles.DOCTOR)
    client = APIClient()
    login = client.post(
        "/api/auth/login/",
        {"username": "doctor1", "password": "testpass123"},
        format="json",
    )
    access = login.data["access"]

    response = client.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Bearer {access}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "doctor1"
    assert response.data["roles"] == [Roles.DOCTOR]
