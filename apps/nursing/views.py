from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Attendance, MedicationAdministrationRecord
from .permissions import AttendancePermission, MedicationAdministrationRecordPermission
from .serializers import AttendanceSerializer, MedicationAdministrationRecordSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("user", "shift")
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]

    def perform_create(self, serializer):
        serializer.save(user=serializer.validated_data.get("user", self.request.user))


class MedicationAdministrationRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicationAdministrationRecord.objects.select_related(
        "patient", "prescription__drug", "administered_by", "dialysis_session"
    )
    serializer_class = MedicationAdministrationRecordSerializer
    permission_classes = [MedicationAdministrationRecordPermission]

    @action(detail=True, methods=["post"])
    def administer(self, request, pk=None):
        """Nurse marks a MAR task as done - the single step that closes
        the loop from 'doctor prescribed' to 'medication actually given'."""
        mar = self.get_object()
        new_status = request.data.get("status", MedicationAdministrationRecord.Status.GIVEN)
        mar.status = new_status
        mar.administered_by = request.user
        mar.administered_at = timezone.now()
        mar.dose_given = request.data.get("dose_given", mar.dose_given)
        mar.notes = request.data.get("notes", mar.notes)
        mar.save(
            update_fields=[
                "status",
                "administered_by",
                "administered_at",
                "dose_given",
                "notes",
            ]
        )
        return Response(MedicationAdministrationRecordSerializer(mar).data)
