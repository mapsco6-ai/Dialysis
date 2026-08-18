from django.db import models

from apps.core.models import BaseModel


class Supplier(BaseModel):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SupplyItem(BaseModel):
    class Category(models.TextChoices):
        MEDICAL_SUPPLY = "medical_supply", "Medical supply"
        MEDICATION_BULK = "medication_bulk", "Medication (bulk, for pharmacy restock)"
        CONSUMABLE = "consumable", "Consumable"
        EQUIPMENT = "equipment", "Equipment"

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices)
    unit_of_measure = models.CharField(max_length=30, help_text="e.g. box, vial, piece")
    reorder_level = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def quantity_on_hand(self):
        return self.stock_batches.aggregate(total=models.Sum("quantity_on_hand"))[
            "total"
        ] or 0


class SupplyStock(BaseModel):
    supply_item = models.ForeignKey(
        SupplyItem, on_delete=models.CASCADE, related_name="stock_batches"
    )
    batch_number = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["expiry_date"]

    def __str__(self):
        return f"{self.supply_item.name} batch {self.batch_number or self.id}"


class StockMovement(BaseModel):
    class MovementType(models.TextChoices):
        IN = "in", "In"
        OUT = "out", "Out"
        ADJUSTMENT = "adjustment", "Adjustment"

    supply_item = models.ForeignKey(
        SupplyItem, on_delete=models.CASCADE, related_name="movements"
    )
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.PositiveIntegerField()
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="movements"
    )
    performed_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    movement_date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(
        max_length=255, blank=True, help_text="Reason, PO number, or related request id"
    )

    class Meta:
        ordering = ["-movement_date"]

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} x {self.supply_item.name}"
