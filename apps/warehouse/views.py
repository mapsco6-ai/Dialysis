from rest_framework import viewsets

from .models import StockMovement, Supplier, SupplyItem, SupplyStock
from .permissions import WarehousePermission
from .serializers import (
    StockMovementSerializer,
    SupplierSerializer,
    SupplyItemSerializer,
    SupplyStockSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [WarehousePermission]


class SupplyItemViewSet(viewsets.ModelViewSet):
    queryset = SupplyItem.objects.all()
    serializer_class = SupplyItemSerializer
    permission_classes = [WarehousePermission]


class SupplyStockViewSet(viewsets.ModelViewSet):
    queryset = SupplyStock.objects.select_related("supply_item")
    serializer_class = SupplyStockSerializer
    permission_classes = [WarehousePermission]


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related("supply_item", "supplier", "performed_by")
    serializer_class = StockMovementSerializer
    permission_classes = [WarehousePermission]

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)
