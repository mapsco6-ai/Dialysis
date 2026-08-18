"""Verifies each role sees exactly the modules docs/permissions.md grants
it, by hitting the list endpoint of one representative resource per
module with every role and asserting 200 (visible) vs 403 (blocked)."""

import pytest
from rest_framework import status

from apps.core.roles import Roles

pytestmark = pytest.mark.django_db

MODULE_ACCESS = {
    "/api/patients/": {
        Roles.DOCTOR: status.HTTP_200_OK,
        Roles.NURSE: status.HTTP_200_OK,
        Roles.PHARMACIST: status.HTTP_200_OK,
        Roles.WAREHOUSE_KEEPER: status.HTTP_403_FORBIDDEN,
        Roles.LAB_TECH: status.HTTP_200_OK,
        Roles.RECEPTIONIST: status.HTTP_200_OK,
    },
    "/api/dialysis-schedules/": {
        Roles.DOCTOR: status.HTTP_200_OK,
        Roles.NURSE: status.HTTP_200_OK,
        Roles.PHARMACIST: status.HTTP_403_FORBIDDEN,
        Roles.WAREHOUSE_KEEPER: status.HTTP_403_FORBIDDEN,
        Roles.LAB_TECH: status.HTTP_403_FORBIDDEN,
        Roles.RECEPTIONIST: status.HTTP_200_OK,
    },
    "/api/drugs/": {
        Roles.DOCTOR: status.HTTP_200_OK,
        Roles.NURSE: status.HTTP_200_OK,
        Roles.PHARMACIST: status.HTTP_200_OK,
        Roles.WAREHOUSE_KEEPER: status.HTTP_403_FORBIDDEN,
        Roles.LAB_TECH: status.HTTP_403_FORBIDDEN,
        Roles.RECEPTIONIST: status.HTTP_403_FORBIDDEN,
    },
    "/api/supply-items/": {
        Roles.DOCTOR: status.HTTP_403_FORBIDDEN,
        Roles.NURSE: status.HTTP_403_FORBIDDEN,
        Roles.PHARMACIST: status.HTTP_200_OK,
        Roles.WAREHOUSE_KEEPER: status.HTTP_200_OK,
        Roles.LAB_TECH: status.HTTP_403_FORBIDDEN,
        Roles.RECEPTIONIST: status.HTTP_403_FORBIDDEN,
    },
    "/api/mar/": {
        Roles.DOCTOR: status.HTTP_200_OK,
        Roles.NURSE: status.HTTP_200_OK,
        Roles.PHARMACIST: status.HTTP_200_OK,
        Roles.WAREHOUSE_KEEPER: status.HTTP_403_FORBIDDEN,
        Roles.LAB_TECH: status.HTTP_403_FORBIDDEN,
        Roles.RECEPTIONIST: status.HTTP_403_FORBIDDEN,
    },
    "/api/lab-orders/": {
        Roles.DOCTOR: status.HTTP_200_OK,
        Roles.NURSE: status.HTTP_200_OK,
        Roles.PHARMACIST: status.HTTP_403_FORBIDDEN,
        Roles.WAREHOUSE_KEEPER: status.HTTP_403_FORBIDDEN,
        Roles.LAB_TECH: status.HTTP_200_OK,
        Roles.RECEPTIONIST: status.HTTP_403_FORBIDDEN,
    },
}

CASES = [
    (url, role, expected)
    for url, per_role in MODULE_ACCESS.items()
    for role, expected in per_role.items()
]


@pytest.mark.parametrize(
    "url,role,expected_status",
    CASES,
    ids=[f"{url}-{role}" for url, role, _ in CASES],
)
def test_module_access_matches_permission_matrix(auth_client, url, role, expected_status):
    client, _ = auth_client(role)
    response = client.get(url)
    assert response.status_code == expected_status


def test_admin_sees_every_module(auth_client):
    client, _ = auth_client(Roles.ADMIN)
    for url in MODULE_ACCESS:
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK, url


def test_unauthenticated_request_is_rejected():
    from rest_framework.test import APIClient

    client = APIClient()
    response = client.get("/api/patients/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
