from rest_framework import serializers

from .models import Attendance, MedicationAdministrationRecord


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class MedicationAdministrationRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    drug_name = serializers.CharField(source="prescription.drug.name", read_only=True)

    class Meta:
        model = MedicationAdministrationRecord
        fields = "__all__"
        read_only_fields = (
            "id",
            "prescription",
            "patient",
            "created_at",
            "updated_at",
        )
