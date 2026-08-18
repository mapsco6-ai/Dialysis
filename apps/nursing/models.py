from django.db import models

from apps.core.models import BaseModel


class Attendance(BaseModel):
    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        LATE = "late", "Late"
        ABSENT = "absent", "Absent"

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="attendance_records"
    )
    shift = models.ForeignKey(
        "scheduling.Shift", on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)

    class Meta:
        ordering = ["-date"]
        unique_together = ("user", "date", "shift")

    def __str__(self):
        return f"{self.user} - {self.date}"


class MedicationAdministrationRecord(BaseModel):
    """The nurse's task list: one row is created automatically for every
    active Prescription (see nursing/signals.py). A nurse may also always
    open a patient's file directly regardless of this list."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        GIVEN = "given", "Given"
        REFUSED = "refused", "Refused"
        MISSED = "missed", "Missed"
        HELD = "held", "Held"

    prescription = models.ForeignKey(
        "pharmacy.Prescription", on_delete=models.CASCADE, related_name="mar_entries"
    )
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="mar_entries"
    )
    dialysis_session = models.ForeignKey(
        "scheduling.DialysisSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mar_entries",
    )
    scheduled_time = models.DateTimeField()
    administered_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mar_entries_administered",
    )
    administered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    dose_given = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["scheduled_time"]

    def __str__(self):
        return f"MAR for {self.patient.mrn} - {self.prescription.drug.name} ({self.status})"
