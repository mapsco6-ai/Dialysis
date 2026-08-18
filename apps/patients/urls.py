from rest_framework.routers import DefaultRouter

from .views import (
    ClinicalNoteViewSet,
    MedicalHistoryViewSet,
    PatientViewSet,
    VascularAccessViewSet,
    VitalSignViewSet,
)

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("medical-histories", MedicalHistoryViewSet, basename="medicalhistory")
router.register("vascular-accesses", VascularAccessViewSet, basename="vascularaccess")
router.register("clinical-notes", ClinicalNoteViewSet, basename="clinicalnote")
router.register("vital-signs", VitalSignViewSet, basename="vitalsign")

urlpatterns = router.urls
