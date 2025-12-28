from django import forms as django_forms
from django.contrib import admin
from . import models


@admin.register(models.SalesMap)
class SalesMapAdmin(admin.ModelAdmin):
    list_display = ("establishment",)
    ordering = ("establishment",)
    readonly_fields = ("id",)
    fieldsets = (
        (
            "Identificação",
            {
                "fields": ("id", "establishment"),
            },
        ),
        (
            "Mapa",
            {
                "fields": ("map",),
            },
        ),
    )


@admin.register(models.GondolaProduct)
class GondolaProductAdmin(admin.ModelAdmin):
    list_display = ("establishment_name", "gondola_name", "product_name")
    ordering = ("gondola__establishment", "gondola__name", "product__name")

    def product_name(self, obj: models.GondolaProduct):
        return obj.product.name

    product_name.short_description = "Produto"

    def establishment_name(self, obj: models.GondolaProduct):
        return obj.gondola.establishment

    establishment_name.short_description = "Estabelecimento"

    def gondola_name(self, obj: models.GondolaProduct):
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
    template = "sales/widgets/gondola_table_editor.html"
    verbose_name = "Produto"
    model = models.GondolaProduct
    extra = 0

    def get_formset(self, request, obj=..., **kwargs):
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


@admin.register(models.Gondola)
class GondolaAdmin(admin.ModelAdmin):
    inlines = [GondolaProductInline]
    list_display = ("name", "establishment")
    ordering = ("establishment", "name")

    def get_readonly_fields(self, request, obj=...):
        fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            fields = list(fields)
            fields.append("establishment")

        return fields


class CartLocatorInline(admin.StackedInline):
    verbose_name = "Localizador"
    verbose_name_plural = "Localizadores"
    model = models.CartLocator
    extra = 0


@admin.register(models.InformationEmissor)
class InformationEmissorAdmin(admin.ModelAdmin):
    inlines = [CartLocatorInline]
    readonly_fields = ("id",)
    list_display = ("id", "establishment", "name")
    ordering = ("establishment", "name")
    fieldsets = (
        (
            "Identificação",
            {
                "fields": ("id", "name", "establishment"),
            },
        ),
        (
            "Autenticação",
            {
                "fields": ("key", "auth"),
            },
        ),
    )


@admin.register(models.CartLocator)
class CartLocatorAdmin(admin.ModelAdmin):
    pass
