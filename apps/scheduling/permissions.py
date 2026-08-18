from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.core.permissions import user_has_role
from apps.core.roles import Roles


class SchedulingPermission(BasePermission):
    """Scheduling/attendance module, per docs/permissions.md:
    - Receptionist: full (create/edit schedules and sessions, check-in).
    - Doctor: view only. Nurse: view + update session status.
    - Everyone else: no access.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or user_has_role(user, Roles.ADMIN):
            return True
        if request.method in SAFE_METHODS:
            return user_has_role(user, Roles.DOCTOR, Roles.NURSE, Roles.RECEPTIONIST)
        if user_has_role(user, Roles.RECEPTIONIST):
            return True
        # Nurse may only update (PATCH/PUT) session status, never create/delete.
        if user_has_role(user, Roles.NURSE) and request.method in ("PATCH", "PUT"):
            return True
        return False
