from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from apps.core.models import BaseModel


class Drug(BaseModel):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, blank=True)
    form = models.CharField(max_length=100, blank=True, help_text="tablet, injection, ...")
    strength = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    requires_prescription = models.BooleanField(default=True)

    warehouse_item = models.ForeignKey(
        "warehouse.SupplyItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_drugs",
        help_text="The warehouse SupplyItem this drug is internally restocked from",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def quantity_on_hand(self):
        return self.stock_batches.aggregate(total=models.Sum("quantity_on_hand"))["total"] or 0


class DrugStock(BaseModel):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name="stock_batches")
    batch_number = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["expiry_date"]

    def __str__(self):
        return f"{self.drug.name} batch {self.batch_number or self.id}"


class Prescription(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="prescriptions"
    )
    prescribing_doctor = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="prescriptions_written"
    )
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name="prescriptions")
    dosage = models.CharField(max_length=100, help_text="e.g. 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g. twice daily")
    route = models.CharField(max_length=50, blank=True, help_text="oral, IV, ...")
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.drug.name} for {self.patient.mrn}"


class DispenseRecord(BaseModel):
    prescription = models.ForeignKey(
        Prescription, on_delete=models.PROTECT, related_name="dispense_records"
    )
    pharmacist = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    drug_stock = models.ForeignKey(DrugStock, on_delete=models.PROTECT)
    quantity_dispensed = models.PositiveIntegerField()
    dispensed_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ["-dispensed_at"]

    def __str__(self):
        return f"Dispensed {self.quantity_dispensed} for {self.prescription}"


class PharmacyStockRequest(BaseModel):
    """Internal supply chain: pharmacy requests drug stock FROM the
    warehouse (the warehouse is pharmacy's internal supplier). Approval by
    a warehouse keeper is required before any stock actually moves - see
    apps/pharmacy/views.py PharmacyStockRequestViewSet.approve()."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        FULFILLED = "fulfilled", "Fulfilled"

    requested_by = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="stock_requests_made"
    )
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name="stock_requests")
    quantity_requested = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_requests_decided",
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return f"Request {self.quantity_requested} x {self.drug.name} ({self.status})"
