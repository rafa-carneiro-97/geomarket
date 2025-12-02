import json
from django.contrib import admin
from django import forms as django_forms
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


@admin.register(models.GondolaProduct)
class GondolaProductAdmin(admin.ModelAdmin):
    list_display = ("establishment_name", "gondola_name", "product_name")
    ordering = ("gondola__establishment", "gondola__name", "product__name")

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Produto"

    def establishment_name(self, obj):
        return obj.gondola.establishment

    establishment_name.short_description = "Estabelecimento"

    def gondola_name(self, obj):
        return obj.gondola.name

    gondola_name.short_description = "Gôndola"

    def get_readonly_fields(self, request, obj=...):
        fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            fields = list(fields)
            fields.append("gondola")
            fields.append("product")

        return fields


class GondolaProductInline(admin.StackedInline):
    template = "business/widgets/gondola_table_editor.html"
    verbose_name = "Produto"
    model = models.GondolaProduct
    extra = 0
    # min_num = 4

    def get_formset(self, request, obj=..., **kwargs):
        print("\n\n\n\n", request.POST)
        return super().get_formset(request, obj, **kwargs)

    @property
    def media(self):
        css = {
            "all": (
                "core/_css/tailwind/output.css",
                "core/_css/admin.css",
            )
        }
        return django_forms.Media(css=css)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product")


@admin.register(models.EstablishmentGondola)
class EstablishmentGondolaAdmin(admin.ModelAdmin):
    inlines = [GondolaProductInline]
    list_display = ("name", "establishment")
    ordering = ("establishment", "name")

    def get_readonly_fields(self, request, obj=...):
        fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            fields = list(fields)
            fields.append("establishment")

        return fields
