from rest_framework import serializers

from .models import ClinicalNote, MedicalHistory, Patient, VascularAccess, VitalSign


class PatientBasicSerializer(serializers.ModelSerializer):
    """Demographics only - used for roles that need to identify a patient
    (Receptionist, LabTech) without exposing the clinical record."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = (
            "id",
            "mrn",
            "full_name",
            "first_name",
            "father_name",
            "grandfather_name",
            "family_name",
            "national_id",
            "date_of_birth",
            "gender",
            "phone",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "registration_date",
            "is_active",
        )
        read_only_fields = ("id", "mrn", "registration_date")


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = "__all__"
        read_only_fields = ("id", "patient", "created_at", "updated_at")


class VascularAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = VascularAccess
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ClinicalNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)

    class Meta:
        model = ClinicalNote
        fields = "__all__"
        read_only_fields = ("id", "author", "created_at", "updated_at")


class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = "__all__"
        read_only_fields = ("id", "recorded_by", "recorded_at")


class PatientFullSerializer(PatientBasicSerializer):
    """Full clinical record - Doctor/Nurse/Admin only."""

    medical_history = MedicalHistorySerializer(read_only=True)
    vascular_accesses = VascularAccessSerializer(many=True, read_only=True)
    clinical_notes = ClinicalNoteSerializer(many=True, read_only=True)
    vital_signs = VitalSignSerializer(many=True, read_only=True)

    class Meta(PatientBasicSerializer.Meta):
        fields = PatientBasicSerializer.Meta.fields + (
            "blood_type",
            "created_by",
            "medical_history",
            "vascular_accesses",
            "clinical_notes",
            "vital_signs",
        )
