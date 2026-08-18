from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.core.permissions import user_has_role
from apps.core.roles import Roles


class AttendancePermission(BasePermission):
    """Nurses manage their own attendance; Admin has full oversight."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        return user_has_role(user, Roles.NURSE)


class MedicationAdministrationRecordPermission(BasePermission):
    """MAR, per docs/permissions.md: Nurse full, Doctor/Pharmacist
    view-only, everyone else no access."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if user_has_role(user, Roles.NURSE):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.PHARMACIST)
        return False
