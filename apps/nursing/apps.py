from django.apps import AppConfig


class NursingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nursing"
    label = "nursing"

    def ready(self):
        from . import signals  # noqa: F401
