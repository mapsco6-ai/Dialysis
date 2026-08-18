from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.core.permissions import user_has_role
from apps.core.roles import Roles


class PatientPermission(BasePermission):
    """Patient/EMR module, per docs/permissions.md:
    - Doctor: full. Receptionist: view + edit demographics.
    - Nurse/Pharmacist/LabTech: view only (basic vs full serializer handles
      which fields they actually see).
    - Warehouse: no access at all.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(
                user,
                Roles.DOCTOR,
                Roles.NURSE,
                Roles.PHARMACIST,
                Roles.LAB_TECH,
                Roles.RECEPTIONIST,
            )
        return user_has_role(user, Roles.DOCTOR, Roles.RECEPTIONIST)


class ClinicalRecordPermission(BasePermission):
    """Medical history, vascular access, clinical notes, vital signs:
    Doctor/Nurse manage the clinical record; everyone else (including
    Receptionist) has no access, per the EMR row of the permission matrix.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        return user_has_role(user, Roles.DOCTOR, Roles.NURSE)
