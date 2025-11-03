from django.contrib import admin
from . import models, forms


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


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


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = forms.EmployeeAdminForm


@admin.register(models.ProductKeyword)
class ProductKeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = forms.ProductAdminForm
    list_display = ("name", "codebar", "is_active")
    ordering = ("is_active", "name")
    search_fields = ("name", "codebar")


@admin.register(models.EstablishmentProduct)
class EstablishmentProductAdmin(admin.ModelAdmin):
    pass
