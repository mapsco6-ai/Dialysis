from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DialysisParameters, DialysisSchedule, DialysisSession, Machine, Shift
from .permissions import SchedulingPermission
from .serializers import (
    DialysisParametersSerializer,
    DialysisScheduleSerializer,
    DialysisSessionSerializer,
    MachineSerializer,
    ShiftSerializer,
)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [SchedulingPermission]


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [SchedulingPermission]


class DialysisScheduleViewSet(viewsets.ModelViewSet):
    queryset = DialysisSchedule.objects.select_related("patient", "preferred_shift")
    serializer_class = DialysisScheduleSerializer
    permission_classes = [SchedulingPermission]

    @action(detail=True, methods=["post"], url_path="check-in")
    def check_in(self, request, pk=None):
        """Create today's DialysisSession for this patient's recurring
        schedule, dynamically assigning a machine/shift based on same-day
        availability - the pairing is never fixed on the schedule itself."""
        schedule = self.get_object()
        shift_id = request.data.get("shift")
        shift = Shift.objects.filter(id=shift_id).first() if shift_id else schedule.preferred_shift
        if shift is None:
            return Response(
                {"detail": "No shift specified and schedule has no preferred_shift."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.localdate()
        busy_machine_ids = (
            DialysisSession.objects.filter(
                scheduled_date=today,
                shift=shift,
            )
            .exclude(status=DialysisSession.Status.CANCELLED)
            .values_list("machine_id", flat=True)
        )
        machine = (
            Machine.objects.filter(status=Machine.Status.AVAILABLE)
            .exclude(id__in=busy_machine_ids)
            .order_by("code")
            .first()
        )
        if machine is None:
            return Response(
                {"detail": "No machine available for this shift today."},
                status=status.HTTP_409_CONFLICT,
            )

        session = DialysisSession.objects.create(
            patient=schedule.patient,
            schedule=schedule,
            machine=machine,
            shift=shift,
            scheduled_date=today,
            check_in_time=timezone.now(),
            status=DialysisSession.Status.CHECKED_IN,
        )
        return Response(DialysisSessionSerializer(session).data, status=status.HTTP_201_CREATED)


class DialysisSessionViewSet(viewsets.ModelViewSet):
    queryset = DialysisSession.objects.select_related(
        "patient", "schedule", "machine", "shift", "assigned_nurse", "assigned_doctor"
    )
    serializer_class = DialysisSessionSerializer
    permission_classes = [SchedulingPermission]


class DialysisParametersViewSet(viewsets.ModelViewSet):
    queryset = DialysisParameters.objects.select_related("session")
    serializer_class = DialysisParametersSerializer
    permission_classes = [SchedulingPermission]
