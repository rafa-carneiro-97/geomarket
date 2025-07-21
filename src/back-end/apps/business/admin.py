from django.contrib import admin
from . import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Emplyee)
class EmplyeeAdmin(admin.ModelAdmin):
    pass
