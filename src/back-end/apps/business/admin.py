from django.contrib import admin
from . import models, forms


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StorePermission)
class StorePermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "codename", "name")
    ordering = ("store",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False


@admin.register(models.StoreGroup)
class StoreGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = forms.EmployeeAdminForm
