from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "full_name",
        "email",
        "employee_id",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_active", "is_staff", "groups")
    search_fields = ("username", "full_name", "email", "employee_id", "national_id")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Staff details",
            {
                "fields": (
                    "full_name",
                    "phone",
                    "national_id",
                    "employee_id",
                    "hire_date",
                )
            },
        ),
    )
