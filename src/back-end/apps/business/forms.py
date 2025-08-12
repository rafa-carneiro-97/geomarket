from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from . import models


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            "permissions": FilteredSelectMultiple("Permissões", is_stacked=False),
            "groups": FilteredSelectMultiple("Grupos", is_stacked=False),
        }
