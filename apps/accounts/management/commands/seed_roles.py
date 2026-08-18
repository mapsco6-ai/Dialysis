from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from apps.core.roles import Roles

# Maps each role to the (app_label, model_name, [codename_actions]) grants it
# needs, per docs/permissions.md. Populated incrementally as each module's
# models are built - a role/module cell not listed here yet simply has no
# grants until that stage lands.
ROLE_MODEL_PERMISSIONS = {
    Roles.DOCTOR: {
        "patients.patient": ["view", "add", "change"],
        "patients.medicalhistory": ["view", "add", "change"],
        "patients.vascularaccess": ["view", "add", "change"],
        "patients.clinicalnote": ["view", "add", "change"],
        "patients.vitalsign": ["view", "add"],
    },
    Roles.NURSE: {
        "patients.patient": ["view"],
        "patients.medicalhistory": ["view"],
        "patients.vascularaccess": ["view"],
        "patients.clinicalnote": ["view", "add"],
        "patients.vitalsign": ["view", "add"],
    },
    Roles.PHARMACIST: {
        "patients.patient": ["view"],
    },
    Roles.LAB_TECH: {
        "patients.patient": ["view"],
    },
    Roles.RECEPTIONIST: {
        "accounts.user": ["view"],
        "patients.patient": ["view", "add", "change"],
    },
}


class Command(BaseCommand):
    help = "Create the system's 7 staff role groups and assign their model permissions."

    def handle(self, *args, **options):
        for role_name in Roles.ALL:
            group, created = Group.objects.get_or_create(name=role_name)
            status = "created" if created else "exists"
            self.stdout.write(f"Group '{role_name}': {status}")

            grants = ROLE_MODEL_PERMISSIONS.get(role_name, {})
            permissions = []
            for app_model, actions in grants.items():
                app_label, model_name = app_model.split(".")
                for action in actions:
                    codename = f"{action}_{model_name}"
                    try:
                        permissions.append(
                            Permission.objects.get(
                                content_type__app_label=app_label,
                                codename=codename,
                            )
                        )
                    except Permission.DoesNotExist:
                        self.stderr.write(
                            f"  Permission {codename} on {app_label} not found - skipping"
                        )
            if permissions:
                group.permissions.set(permissions)

        # Admin group gets full Django admin access via is_superuser on the
        # user account, not via group permissions - group membership is
        # still used for module visibility checks in the frontend.
        self.stdout.write(self.style.SUCCESS("Roles seeded."))
