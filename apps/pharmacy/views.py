from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.core.permissions import user_has_role
from apps.core.roles import Roles
from apps.warehouse.models import StockMovement, SupplyStock

from .models import DispenseRecord, Drug, DrugStock, PharmacyStockRequest, Prescription
from .permissions import (
    DispenseRecordPermission,
    DrugCatalogPermission,
    PharmacyStockRequestPermission,
    PrescriptionPermission,
)
from .serializers import (
    DispenseRecordSerializer,
    DrugSerializer,
    DrugStockSerializer,
    PharmacyStockRequestSerializer,
    PrescriptionSerializer,
)


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [DrugCatalogPermission]


class DrugStockViewSet(viewsets.ModelViewSet):
    queryset = DrugStock.objects.select_related("drug")
    serializer_class = DrugStockSerializer
    permission_classes = [DrugCatalogPermission]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related("patient", "prescribing_doctor", "drug")
    serializer_class = PrescriptionSerializer
    permission_classes = [PrescriptionPermission]

    def perform_create(self, serializer):
        serializer.save(prescribing_doctor=self.request.user)


class DispenseRecordViewSet(viewsets.ModelViewSet):
    queryset = DispenseRecord.objects.select_related("prescription", "pharmacist", "drug_stock")
    serializer_class = DispenseRecordSerializer
    permission_classes = [DispenseRecordPermission]

    def perform_create(self, serializer):
        drug_stock = serializer.validated_data["drug_stock"]
        quantity = serializer.validated_data["quantity_dispensed"]
        if drug_stock.quantity_on_hand < quantity:
            raise PermissionDenied("Insufficient stock in this batch to dispense that quantity.")
        with transaction.atomic():
            drug_stock.quantity_on_hand -= quantity
            drug_stock.save(update_fields=["quantity_on_hand"])
            serializer.save(pharmacist=self.request.user)


class PharmacyStockRequestViewSet(viewsets.ModelViewSet):
    queryset = PharmacyStockRequest.objects.select_related("drug", "requested_by", "approved_by")
    serializer_class = PharmacyStockRequestSerializer
    permission_classes = [PharmacyStockRequestPermission]

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Warehouse keeper approves: stock physically moves from the
        warehouse's SupplyStock to the pharmacy's DrugStock in one
        transaction. This is the internal supplier hand-off the pharmacist
        cannot trigger themselves."""
        if not user_has_role(request.user, Roles.ADMIN, Roles.WAREHOUSE_KEEPER):
            raise PermissionDenied("Only a warehouse keeper can approve a stock request.")

        stock_request = self.get_object()
        if stock_request.status != PharmacyStockRequest.Status.PENDING:
            return Response(
                {"detail": f"Request is already {stock_request.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        warehouse_item = stock_request.drug.warehouse_item
        if warehouse_item is None:
            return Response(
                {"detail": "This drug has no linked warehouse supply item to draw from."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantity_needed = stock_request.quantity_requested
        available = warehouse_item.quantity_on_hand
        if available < quantity_needed:
            return Response(
                {
                    "detail": (
                        f"Insufficient warehouse stock: {available} available, "
                        f"{quantity_needed} requested."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        with transaction.atomic():
            remaining = quantity_needed
            batches = (
                SupplyStock.objects.select_for_update()
                .filter(supply_item=warehouse_item, quantity_on_hand__gt=0)
                .order_by("expiry_date")
            )
            for batch in batches:
                if remaining <= 0:
                    break
                take = min(batch.quantity_on_hand, remaining)
                batch.quantity_on_hand -= take
                batch.save(update_fields=["quantity_on_hand"])
                remaining -= take

            StockMovement.objects.create(
                supply_item=warehouse_item,
                movement_type=StockMovement.MovementType.OUT,
                quantity=quantity_needed,
                performed_by=request.user,
                reference=f"PharmacyStockRequest {stock_request.id}",
            )

            DrugStock.objects.create(
                drug=stock_request.drug,
                batch_number=f"INTERNAL-{stock_request.id}",
                quantity_on_hand=quantity_needed,
            )

            now = timezone.now()
            stock_request.status = PharmacyStockRequest.Status.FULFILLED
            stock_request.approved_by = request.user
            stock_request.decided_at = now
            stock_request.fulfilled_at = now
            stock_request.save(
                update_fields=["status", "approved_by", "decided_at", "fulfilled_at"]
            )

        return Response(PharmacyStockRequestSerializer(stock_request).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        if not user_has_role(request.user, Roles.ADMIN, Roles.WAREHOUSE_KEEPER):
            raise PermissionDenied("Only a warehouse keeper can reject a stock request.")

        stock_request = self.get_object()
        if stock_request.status != PharmacyStockRequest.Status.PENDING:
            return Response(
                {"detail": f"Request is already {stock_request.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        stock_request.status = PharmacyStockRequest.Status.REJECTED
        stock_request.approved_by = request.user
        stock_request.decided_at = timezone.now()
        stock_request.notes = request.data.get("reason", stock_request.notes)
        stock_request.save(update_fields=["status", "approved_by", "decided_at", "notes"])
        return Response(PharmacyStockRequestSerializer(stock_request).data)
