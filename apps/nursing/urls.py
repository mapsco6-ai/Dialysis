from rest_framework.routers import DefaultRouter

from .views import AttendanceViewSet, MedicationAdministrationRecordViewSet

router = DefaultRouter()
router.register("attendance", AttendanceViewSet, basename="attendance")
router.register("mar", MedicationAdministrationRecordViewSet, basename="mar")

urlpatterns = router.urls
