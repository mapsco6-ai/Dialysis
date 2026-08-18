from rest_framework import viewsets

from apps.core.permissions import user_has_role
from apps.core.roles import Roles

from .models import ClinicalNote, MedicalHistory, Patient, VascularAccess, VitalSign
from .permissions import ClinicalRecordPermission, PatientPermission
from .serializers import (
    ClinicalNoteSerializer,
    MedicalHistorySerializer,
    PatientBasicSerializer,
    PatientFullSerializer,
    VascularAccessSerializer,
    VitalSignSerializer,
)

FULL_RECORD_ROLES = (Roles.DOCTOR, Roles.NURSE)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = [PatientPermission]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser or user_has_role(user, Roles.ADMIN, *FULL_RECORD_ROLES):
            return PatientFullSerializer
        return PatientBasicSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.select_related("patient")
    serializer_class = MedicalHistorySerializer
    permission_classes = [ClinicalRecordPermission]


class VascularAccessViewSet(viewsets.ModelViewSet):
    queryset = VascularAccess.objects.select_related("patient")
    serializer_class = VascularAccessSerializer
    permission_classes = [ClinicalRecordPermission]


class ClinicalNoteViewSet(viewsets.ModelViewSet):
    queryset = ClinicalNote.objects.select_related("patient", "author")
    serializer_class = ClinicalNoteSerializer
    permission_classes = [ClinicalRecordPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.select_related("patient", "recorded_by")
    serializer_class = VitalSignSerializer
    permission_classes = [ClinicalRecordPermission]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)
