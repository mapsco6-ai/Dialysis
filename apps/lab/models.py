from django.db import models

from apps.core.models import BaseModel


class LabTestType(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=30, unique=True)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=30, blank=True)
    reference_range_low = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )
    reference_range_high = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True
    )
    sample_type = models.CharField(max_length=50, blank=True, help_text="blood, urine, ...")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class LabOrder(BaseModel):
    class Status(models.TextChoices):
        ORDERED = "ordered", "Ordered"
        SAMPLE_COLLECTED = "sample_collected", "Sample collected"
        RESULTED = "resulted", "Resulted"
        CANCELLED = "cancelled", "Cancelled"

    class Priority(models.TextChoices):
        ROUTINE = "routine", "Routine"
        URGENT = "urgent", "Urgent"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="lab_orders"
    )
    ordering_doctor = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="lab_orders_placed"
    )
    test_type = models.ForeignKey(LabTestType, on_delete=models.PROTECT, related_name="orders")
    dialysis_session = models.ForeignKey(
        "scheduling.DialysisSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lab_orders",
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDERED)
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.ROUTINE
    )

    class Meta:
        ordering = ["-order_date"]

    def __str__(self):
        return f"{self.test_type.code} for {self.patient.mrn}"


class LabResult(BaseModel):
    class Source(models.TextChoices):
        MANUAL = "manual", "Manual entry"
        INSTRUMENT = "instrument", "Instrument (automated)"

    lab_order = models.OneToOneField(LabOrder, on_delete=models.CASCADE, related_name="result")
    result_value = models.CharField(max_length=100)
    unit = models.CharField(max_length=30, blank=True)
    is_abnormal = models.BooleanField(default=False)
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lab_results_performed",
    )
    verified_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lab_results_verified",
    )
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.MANUAL)
    result_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-result_date"]

    def __str__(self):
        return f"Result for {self.lab_order}"
