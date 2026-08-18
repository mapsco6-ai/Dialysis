from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RoleAwareTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds the user's role group names to the JWT payload so the frontend
    can render the correct module set without an extra round trip."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["roles"] = list(user.groups.values_list("name", flat=True))
        token["full_name"] = user.full_name
        return token


class MeSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "full_name",
            "email",
            "phone",
            "employee_id",
            "roles",
        )

    def get_roles(self, obj) -> list[str]:
        return list(obj.groups.values_list("name", flat=True))
