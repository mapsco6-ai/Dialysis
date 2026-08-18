from django.contrib import admin

from .models import Attendance, MedicationAdministrationRecord


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "shift", "status", "check_in_time", "check_out_time")
    list_filter = ("status", "shift")
    search_fields = ("user__username", "user__full_name")


@admin.register(MedicationAdministrationRecord)
class MedicationAdministrationRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "prescription",
        "status",
        "scheduled_time",
        "administered_by",
        "administered_at",
    )
    list_filter = ("status",)
    search_fields = ("patient__mrn",)
