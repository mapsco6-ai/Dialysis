from django.contrib import admin

from .models import ClinicalNote, MedicalHistory, Patient, VascularAccess, VitalSign


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("mrn", "full_name", "gender", "date_of_birth", "phone", "is_active")
    search_fields = ("mrn", "first_name", "father_name", "family_name", "national_id", "phone")
    list_filter = ("gender", "blood_type", "is_active")
    readonly_fields = ("mrn", "registration_date")


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("patient", "bloodborne_virus_status", "dialysis_start_date")
    list_filter = ("bloodborne_virus_status",)
    search_fields = ("patient__mrn", "patient__first_name", "patient__family_name")


@admin.register(VascularAccess)
class VascularAccessAdmin(admin.ModelAdmin):
    list_display = ("patient", "access_type", "site", "status", "creation_date")
    list_filter = ("access_type", "status")
    search_fields = ("patient__mrn",)


@admin.register(ClinicalNote)
class ClinicalNoteAdmin(admin.ModelAdmin):
    list_display = ("patient", "author", "note_type", "created_at")
    list_filter = ("note_type",)
    search_fields = ("patient__mrn", "content")


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ("patient", "recorded_by", "recorded_at", "weight_pre_kg", "weight_post_kg")
    search_fields = ("patient__mrn",)
