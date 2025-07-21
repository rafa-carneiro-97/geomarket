from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from django.contrib.auth.models import Group
from . import models


admin.site.unregister(Group)


@admin.register(models.CustomPermissionGroup)
class CustomPermissionGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(get_user_model())
class UserAdmin(auth_admin.UserAdmin):
    model = get_user_model()
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
        "is_email_verified",
        "created_at",
    )
    ordering = (
        "-is_superuser",
        "-is_staff",
        "-is_active",
        "-is_email_verified",
        "created_at",
    )
    list_filter = ("email", "created_at")
    search_fields = ("email",)
    readonly_fields = ("id", "is_superuser", "last_login")
    add_fieldsets = (
        (
            "Identificação",
            {
                "fields": ("photo", ("first_name", "last_name")),
            },
        ),
        (
            "Dados de login",
            {"fields": ("email", "is_email_verified", "password1", "password2")},
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    fieldsets = (
        (
            "Identificação",
            {
                "fields": (
                    "id",
                    ("first_name", "last_name"),
                ),
            },
        ),
        (
            "Dados de login",
            {"fields": ("email", "is_email_verified", "password", "last_login")},
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
