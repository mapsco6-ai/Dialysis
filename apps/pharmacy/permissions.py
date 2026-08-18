from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.core.permissions import user_has_role
from apps.core.roles import Roles


class DrugCatalogPermission(BasePermission):
    """Drug / DrugStock: Pharmacist full, Doctor/Nurse view-only
    (they need the catalog to prescribe / track MAR), everyone else none.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if user_has_role(user, Roles.PHARMACIST):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.NURSE)
        return False


class PrescriptionPermission(BasePermission):
    """Prescription: Doctor may create/view (writes a prescription during
    rounds); Pharmacist/Nurse view-only; nobody deletes a prescription
    (clinical record) outside Admin.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.PHARMACIST, Roles.NURSE)
        if request.method == "DELETE":
            return False
        return user_has_role(user, Roles.DOCTOR)


class DispenseRecordPermission(BasePermission):
    """DispenseRecord: Pharmacist full, everyone else (besides Admin) no
    access - dispensing is the pharmacist's exclusive action."""

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        return user_has_role(user, Roles.PHARMACIST)


class PharmacyStockRequestPermission(BasePermission):
    """PharmacyStockRequest: Pharmacist creates/views; WarehouseKeeper
    views and approves/reject via the dedicated actions (never a generic
    PATCH, since a pharmacist must not be able to self-approve).
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.PHARMACIST, Roles.WAREHOUSE_KEEPER)
        if request.method == "POST" and view.action == "create":
            return user_has_role(user, Roles.PHARMACIST)
        # approve/reject are custom actions checked separately in the view
        return user_has_role(user, Roles.WAREHOUSE_KEEPER)
