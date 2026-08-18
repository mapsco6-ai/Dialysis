from rest_framework import viewsets

from .models import LabOrder, LabResult, LabTestType
from .permissions import LabOrderPermission, LabResultPermission, LabTestTypeCatalogPermission
from .serializers import LabOrderSerializer, LabResultSerializer, LabTestTypeSerializer


class LabTestTypeViewSet(viewsets.ModelViewSet):
    queryset = LabTestType.objects.all()
    serializer_class = LabTestTypeSerializer
    permission_classes = [LabTestTypeCatalogPermission]


class LabOrderViewSet(viewsets.ModelViewSet):
    queryset = LabOrder.objects.select_related("patient", "ordering_doctor", "test_type")
    serializer_class = LabOrderSerializer
    permission_classes = [LabOrderPermission]

    def perform_create(self, serializer):
        serializer.save(ordering_doctor=self.request.user)


class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.select_related("lab_order")
    serializer_class = LabResultSerializer
    permission_classes = [LabResultPermission]

    def perform_create(self, serializer):
        # Manual entry is the only supported path today; `source` defaults
        # to LabResult.Source.MANUAL. When instrument integration lands,
        # that feed will set source=INSTRUMENT instead - no model change
        # needed.
        result = serializer.save(performed_by=self.request.user)
        lab_order = result.lab_order
        lab_order.status = LabOrder.Status.RESULTED
        lab_order.save(update_fields=["status"])
