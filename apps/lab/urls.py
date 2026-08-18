from rest_framework.routers import DefaultRouter

from .views import LabOrderViewSet, LabResultViewSet, LabTestTypeViewSet

router = DefaultRouter()
router.register("lab-test-types", LabTestTypeViewSet, basename="labtesttype")
router.register("lab-orders", LabOrderViewSet, basename="laborder")
router.register("lab-results", LabResultViewSet, basename="labresult")

urlpatterns = router.urls
