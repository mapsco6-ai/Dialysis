from django.contrib import admin

from .models import StockMovement, Supplier, SupplyItem, SupplyStock


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "phone", "email")
    search_fields = ("name", "contact_person")


@admin.register(SupplyItem)
class SupplyItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "unit_of_measure", "reorder_level", "quantity_on_hand")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(SupplyStock)
class SupplyStockAdmin(admin.ModelAdmin):
    list_display = ("supply_item", "batch_number", "expiry_date", "quantity_on_hand", "location")
    list_filter = ("supply_item",)
    search_fields = ("supply_item__name", "batch_number")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "supply_item",
        "movement_type",
        "quantity",
        "performed_by",
        "movement_date",
    )
    list_filter = ("movement_type",)
    search_fields = ("supply_item__name", "reference")
