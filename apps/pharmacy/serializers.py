from rest_framework import serializers

from .models import DispenseRecord, Drug, DrugStock, PharmacyStockRequest, Prescription


class DrugSerializer(serializers.ModelSerializer):
    quantity_on_hand = serializers.IntegerField(read_only=True)

    class Meta:
        model = Drug
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class DrugStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugStock
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class PrescriptionSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source="drug.name", read_only=True)
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"
        read_only_fields = ("id", "prescribing_doctor", "created_at", "updated_at")


class DispenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispenseRecord
        fields = "__all__"
        read_only_fields = ("id", "pharmacist", "dispensed_at", "created_at", "updated_at")


class PharmacyStockRequestSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source="drug.name", read_only=True)

    class Meta:
        model = PharmacyStockRequest
        fields = "__all__"
        read_only_fields = (
            "id",
            "requested_by",
            "status",
            "approved_by",
            "requested_at",
            "decided_at",
            "fulfilled_at",
            "created_at",
            "updated_at",
        )
