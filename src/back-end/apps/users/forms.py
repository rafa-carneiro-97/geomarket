from django import forms
from . import models


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = "__all__"
