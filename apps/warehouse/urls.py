from rest_framework.routers import DefaultRouter

from .views import StockMovementViewSet, SupplierViewSet, SupplyItemViewSet, SupplyStockViewSet

router = DefaultRouter()
router.register("suppliers", SupplierViewSet, basename="supplier")
router.register("supply-items", SupplyItemViewSet, basename="supplyitem")
router.register("supply-stock", SupplyStockViewSet, basename="supplystock")
router.register("stock-movements", StockMovementViewSet, basename="stockmovement")

urlpatterns = router.urls
