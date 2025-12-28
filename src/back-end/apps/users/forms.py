from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from . import models


class UserAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = models.User
        fields = "__all__"


class UserAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = ("email",)
