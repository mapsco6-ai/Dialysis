from django.contrib import admin

from .models import DispenseRecord, Drug, DrugStock, PharmacyStockRequest, Prescription


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ("name", "generic_name", "form", "strength", "requires_prescription")
    search_fields = ("name", "generic_name")
    list_filter = ("requires_prescription", "category")


@admin.register(DrugStock)
class DrugStockAdmin(admin.ModelAdmin):
    list_display = ("drug", "batch_number", "expiry_date", "quantity_on_hand", "location")
    search_fields = ("drug__name", "batch_number")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "drug", "prescribing_doctor", "status", "start_date")
    list_filter = ("status",)
    search_fields = ("patient__mrn", "drug__name")


@admin.register(DispenseRecord)
class DispenseRecordAdmin(admin.ModelAdmin):
    list_display = ("prescription", "pharmacist", "quantity_dispensed", "dispensed_at")
    search_fields = ("prescription__patient__mrn",)


@admin.register(PharmacyStockRequest)
class PharmacyStockRequestAdmin(admin.ModelAdmin):
    list_display = (
        "drug",
        "quantity_requested",
        "requested_by",
        "status",
        "approved_by",
        "requested_at",
    )
    list_filter = ("status",)
    search_fields = ("drug__name",)
