from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.core.permissions import user_has_role
from apps.core.roles import Roles


class LabTestTypeCatalogPermission(BasePermission):
    """Test type catalog: LabTech manages it, Doctor/Nurse read it to
    place/view orders."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if user_has_role(user, Roles.LAB_TECH):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.NURSE)
        return False


class LabOrderPermission(BasePermission):
    """LabOrder, per docs/permissions.md: Doctor creates/views, LabTech
    full, Nurse view-only, everyone else no access."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if user_has_role(user, Roles.LAB_TECH):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.NURSE)
        return user_has_role(user, Roles.DOCTOR)


class LabResultPermission(BasePermission):
    """LabResult: LabTech full (manual entry today, instrument-fed later
    without changing this permission), Doctor/Nurse view-only."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if user_has_role(user, Roles.LAB_TECH):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.NURSE)
        return False
