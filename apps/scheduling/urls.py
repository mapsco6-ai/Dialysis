from rest_framework.routers import DefaultRouter

from .views import (
    DialysisParametersViewSet,
    DialysisScheduleViewSet,
    DialysisSessionViewSet,
    MachineViewSet,
    ShiftViewSet,
)

router = DefaultRouter()
router.register("machines", MachineViewSet, basename="machine")
router.register("shifts", ShiftViewSet, basename="shift")
router.register("dialysis-schedules", DialysisScheduleViewSet, basename="dialysisschedule")
router.register("dialysis-sessions", DialysisSessionViewSet, basename="dialysissession")
router.register("dialysis-parameters", DialysisParametersViewSet, basename="dialysisparameters")

urlpatterns = router.urls
