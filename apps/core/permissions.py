from rest_framework.permissions import BasePermission

from .roles import Roles


def user_has_role(user, *role_names):
    if not (user and user.is_authenticated):
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=role_names).exists()


def role_permission_class(*role_names):
    """Build a DRF permission class granting access to the given roles
    (Admin is always implicitly allowed)."""

    class _RolePermission(BasePermission):
        def has_permission(self, request, view):
            return user_has_role(request.user, Roles.ADMIN, *role_names)

    return _RolePermission


IsAdmin = role_permission_class()
IsDoctor = role_permission_class(Roles.DOCTOR)
IsNurse = role_permission_class(Roles.NURSE)
IsPharmacist = role_permission_class(Roles.PHARMACIST)
IsWarehouseKeeper = role_permission_class(Roles.WAREHOUSE_KEEPER)
IsLabTech = role_permission_class(Roles.LAB_TECH)
IsReceptionist = role_permission_class(Roles.RECEPTIONIST)
