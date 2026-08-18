from django.contrib import admin

from .models import DialysisParameters, DialysisSchedule, DialysisSession, Machine, Shift


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("code", "room", "status")
    list_filter = ("status",)
    search_fields = ("code", "room")


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time")


@admin.register(DialysisSchedule)
class DialysisScheduleAdmin(admin.ModelAdmin):
    list_display = ("patient", "preferred_shift", "start_date", "end_date", "status")
    list_filter = ("status", "preferred_shift")
    search_fields = ("patient__mrn",)


@admin.register(DialysisSession)
class DialysisSessionAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "scheduled_date",
        "machine",
        "shift",
        "status",
        "assigned_nurse",
        "assigned_doctor",
    )
    list_filter = ("status", "scheduled_date", "shift", "machine")
    search_fields = ("patient__mrn",)


@admin.register(DialysisParameters)
class DialysisParametersAdmin(admin.ModelAdmin):
    list_display = ("session", "blood_flow_rate_ml_min", "uf_target_ml", "duration_minutes")
