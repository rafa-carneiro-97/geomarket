from django import forms
from django.contrib.auth import forms as auth_forms
from apps.users import models as user_models


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    stay_connected = forms.BooleanField(required=False)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        self.user_cache: user_models.User = user_models.User.objects.filter(
            email=username
        ).first()

        if self.user_cache is None:
            raise self.get_invalid_login_error()

        if not self.user_cache.check_password(password):
            raise self.get_invalid_login_error()

        self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
