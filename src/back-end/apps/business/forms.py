from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import QuerySet
from . import models


class EstablishmentGroupAdminForm(forms.ModelForm):
    class Meta:
        model = models.EstablishmentGroup
        fields = "__all__"
        widgets = {
            "permissions": FilteredSelectMultiple("Permissões", is_stacked=False),
        }

    def clean(self):
        cleaned_data = super().clean()
        establishment = cleaned_data.get("establishment")
        permissions: QuerySet[models.EstablishmentPermission] = cleaned_data.get(
            "permissions"
        )

        if permissions:
            # Ensure all permissions belong to the same establishment
            is_invalid = permissions.exclude(establishment=establishment).exists()

            if is_invalid:
                raise forms.ValidationError(
                    {
                        "permissions": "Todos as pemissões do grupo devem pertencer à mesma loja do mesmo."
                    }
                )

        return cleaned_data


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            "permissions": FilteredSelectMultiple("Permissões", is_stacked=False),
            "groups": FilteredSelectMultiple("Grupos", is_stacked=False),
        }

    def clean(self):
        cleaned_data = super().clean()
        establishment = cleaned_data.get("establishment")

        permissions: QuerySet[models.EstablishmentPermission] = cleaned_data.get(
            "permissions"
        )
        if permissions:
            is_invalid = permissions.exclude(establishment=establishment).exists()

            if is_invalid:
                raise forms.ValidationError(
                    {
                        "permissions": "Todos as pemissões do ufncionário devem pertencer à mesma loja do mesmo."
                    }
                )

        groups: QuerySet[models.EstablishmentGroup] = cleaned_data.get("groups")

        for item in groups:
            if item.establishment.id != establishment:
                raise forms.ValidationError(
                    {
                        "groups": "Todos os grupos do ufncionário devem pertencer à mesma loja do mesmo."
                    }
                )

        return cleaned_data


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = "__all__"
        widgets = {
            "keywords": FilteredSelectMultiple("Palavras-chave", is_stacked=False),
        }
