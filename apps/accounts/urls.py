from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MeView, RoleAwareTokenObtainPairView

urlpatterns = [
    path("auth/login/", RoleAwareTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
]
