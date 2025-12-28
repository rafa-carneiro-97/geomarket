import json
from django.contrib import admin
from . import models, forms


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = forms.ProductAdminForm
    list_display = ("id", "name", "barcode", "is_active")
    ordering = ("is_active", "name")
    search_fields = ("name", "barcode")


@admin.register(models.Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EstablishmentPermission)
class EstablishmentPermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "establishment", "codename", "name")
    ordering = ("establishment",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False


@admin.register(models.EstablishmentGroup)
class EstablishmentGroupAdmin(admin.ModelAdmin):
    form = forms.EstablishmentGroupAdminForm


@admin.register(models.EstablishmentEmployee)
class EstablishmentEmployeeAdmin(admin.ModelAdmin):
    form = forms.EstablishmentEmployeeAdminForm


@admin.register(models.ProductKeyword)
class ProductKeywordAdmin(admin.ModelAdmin):
    pass
