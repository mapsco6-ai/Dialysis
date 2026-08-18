from rest_framework import serializers

from .models import LabOrder, LabResult, LabTestType


class LabTestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestType
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = "__all__"
        read_only_fields = (
            "id",
            "performed_by",
            "source",
            "result_date",
            "created_at",
            "updated_at",
        )


class LabOrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    test_type_name = serializers.CharField(source="test_type.name", read_only=True)
    result = LabResultSerializer(read_only=True)

    class Meta:
        model = LabOrder
        fields = "__all__"
        read_only_fields = ("id", "ordering_doctor", "order_date", "created_at", "updated_at")
