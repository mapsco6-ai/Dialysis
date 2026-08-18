from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import BaseModel


class Patient(BaseModel):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    class BloodType(models.TextChoices):
        A_POS = "A+", "A+"
        A_NEG = "A-", "A-"
        B_POS = "B+", "B+"
        B_NEG = "B-", "B-"
        AB_POS = "AB+", "AB+"
        AB_NEG = "AB-", "AB-"
        O_POS = "O+", "O+"
        O_NEG = "O-", "O-"
        UNKNOWN = "UNK", "Unknown"

    mrn = models.CharField(max_length=20, unique=True, editable=False)

    first_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True)
    grandfather_name = models.CharField(max_length=100, blank=True)
    family_name = models.CharField(max_length=100, blank=True)

    national_id = models.CharField(max_length=32, blank=True, db_index=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    blood_type = models.CharField(
        max_length=3, choices=BloodType.choices, default=BloodType.UNKNOWN
    )

    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients_registered",
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ["-registration_date"]

    def __str__(self):
        return f"{self.mrn} - {self.full_name}"

    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.father_name, self.grandfather_name, self.family_name]
        return " ".join(p for p in parts if p)

    def save(self, *args, **kwargs):
        if not self.mrn:
            self.mrn = self._generate_mrn()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_mrn():
        from django.db.models import Max

        last = Patient.objects.aggregate(Max("mrn"))["mrn__max"]
        next_number = 1
        if last and last.startswith("MRN"):
            try:
                next_number = int(last.removeprefix("MRN")) + 1
            except ValueError:
                pass
        return f"MRN{next_number:06d}"


class MedicalHistory(BaseModel):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name="medical_history"
    )
    comorbidities = models.TextField(blank=True, help_text="Comma-separated or free text")
    allergies = models.TextField(blank=True)
    cause_of_kidney_failure = models.CharField(max_length=255, blank=True)
    dialysis_start_date = models.DateField(null=True, blank=True)

    class BloodBorneStatus(models.TextChoices):
        NEGATIVE = "negative", "Negative"
        HBV = "hbv", "Hepatitis B"
        HCV = "hcv", "Hepatitis C"
        HIV = "hiv", "HIV"

    bloodborne_virus_status = models.CharField(
        max_length=20,
        choices=BloodBorneStatus.choices,
        default=BloodBorneStatus.NEGATIVE,
        help_text="Relevant for dialysis machine isolation protocol",
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Medical history - {self.patient.mrn}"


class VascularAccess(BaseModel):
    class AccessType(models.TextChoices):
        FISTULA = "fistula", "Fistula"
        GRAFT = "graft", "Graft"
        CATHETER = "catheter", "Catheter"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        FAILED = "failed", "Failed"
        REMOVED = "removed", "Removed"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vascular_accesses")
    access_type = models.CharField(max_length=20, choices=AccessType.choices)
    site = models.CharField(max_length=100, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f"{self.get_access_type_display()} - {self.patient.mrn}"


class ClinicalNote(BaseModel):
    class NoteType(models.TextChoices):
        ROUND = "round", "Doctor round"
        GENERAL = "general", "General"
        NURSING = "nursing", "Nursing"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="clinical_notes")
    author = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    note_type = models.CharField(max_length=20, choices=NoteType.choices, default=NoteType.GENERAL)
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note on {self.patient.mrn} by {self.author}"


class VitalSign(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="vital_signs")
    session = models.ForeignKey(
        "scheduling.DialysisSession",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vital_signs",
    )
    recorded_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT)

    weight_pre_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_post_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure_pre = models.CharField(max_length=20, blank=True, help_text="e.g. 130/80")
    blood_pressure_post = models.CharField(max_length=20, blank=True)
    pulse = models.PositiveIntegerField(null=True, blank=True)
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"Vitals for {self.patient.mrn} at {self.recorded_at:%Y-%m-%d %H:%M}"
