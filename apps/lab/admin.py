from django.contrib import admin

from .models import LabOrder, LabResult, LabTestType


@admin.register(LabTestType)
class LabTestTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category", "unit", "sample_type")
    search_fields = ("name", "code")


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "test_type",
        "ordering_doctor",
        "status",
        "priority",
        "order_date",
    )
    list_filter = ("status", "priority")
    search_fields = ("patient__mrn", "test_type__name")


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = (
        "lab_order",
        "result_value",
        "unit",
        "is_abnormal",
        "source",
        "result_date",
    )
    list_filter = ("source", "is_abnormal")
