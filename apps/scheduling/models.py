from django.db import models

from apps.core.models import BaseModel


class Machine(BaseModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        IN_USE = "in_use", "In use"
        MAINTENANCE = "maintenance", "Under maintenance"
        OUT_OF_SERVICE = "out_of_service", "Out of service"

    code = models.CharField(max_length=20, unique=True)
    room = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Shift(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.name} ({self.start_time:%H:%M}-{self.end_time:%H:%M})"


class DialysisSchedule(BaseModel):
    """The recurring template: WHEN a patient is expected, not WHERE.
    Machine/bed assignment happens dynamically per-session at check-in."""

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        ENDED = "ended", "Ended"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="dialysis_schedules"
    )
    days_of_week = models.JSONField(
        default=list, help_text="List of Weekday integers, e.g. [0, 2, 5] for Mon/Wed/Sat"
    )
    preferred_shift = models.ForeignKey(
        Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    session_duration_minutes = models.PositiveIntegerField(default=240)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"Schedule for {self.patient.mrn}"


class DialysisSession(BaseModel):
    """The actual occurrence, created when a patient checks in. Machine and
    shift are assigned HERE, dynamically, based on same-day availability -
    never inherited as a fixed pairing from the schedule template."""

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        CHECKED_IN = "checked_in", "Checked in"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        NO_SHOW = "no_show", "No show"

    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.CASCADE, related_name="dialysis_sessions"
    )
    schedule = models.ForeignKey(
        DialysisSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions",
        help_text="Null for an unscheduled/walk-in session",
    )
    machine = models.ForeignKey(
        Machine, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    shift = models.ForeignKey(
        Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )

    scheduled_date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)

    assigned_nurse = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dialysis_sessions_as_nurse",
    )
    assigned_doctor = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dialysis_sessions_as_doctor",
    )

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return f"Session {self.patient.mrn} on {self.scheduled_date}"


class DialysisParameters(BaseModel):
    session = models.OneToOneField(
        DialysisSession, on_delete=models.CASCADE, related_name="parameters"
    )
    blood_flow_rate_ml_min = models.PositiveIntegerField(null=True, blank=True)
    dialysate_flow_rate_ml_min = models.PositiveIntegerField(null=True, blank=True)
    uf_target_ml = models.PositiveIntegerField(null=True, blank=True)
    uf_actual_ml = models.PositiveIntegerField(null=True, blank=True)
    anticoagulant = models.CharField(max_length=100, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Parameters for session {self.session_id}"
