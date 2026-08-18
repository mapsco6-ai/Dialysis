from rest_framework.routers import DefaultRouter

from .views import (
    DispenseRecordViewSet,
    DrugStockViewSet,
    DrugViewSet,
    PharmacyStockRequestViewSet,
    PrescriptionViewSet,
)

router = DefaultRouter()
router.register("drugs", DrugViewSet, basename="drug")
router.register("drug-stock", DrugStockViewSet, basename="drugstock")
router.register("prescriptions", PrescriptionViewSet, basename="prescription")
router.register("dispense-records", DispenseRecordViewSet, basename="dispenserecord")
router.register(
    "pharmacy-stock-requests", PharmacyStockRequestViewSet, basename="pharmacystockrequest"
)

urlpatterns = router.urls
