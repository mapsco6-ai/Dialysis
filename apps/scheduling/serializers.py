from rest_framework import serializers

from .models import DialysisParameters, DialysisSchedule, DialysisSession, Machine, Shift


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class DialysisScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialysisSchedule
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class DialysisParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialysisParameters
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class DialysisSessionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    parameters = DialysisParametersSerializer(read_only=True)

    class Meta:
        model = DialysisSession
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
