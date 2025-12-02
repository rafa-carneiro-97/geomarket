from django import forms
from django.contrib.auth import forms as auth_forms
from apps.business import models as business_models
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


class CustomUserCreationForm(auth_forms.UserCreationForm):
    email2 = forms.EmailField(required=True)

    class Meta(auth_forms.UserChangeForm.Meta):
        model = user_models.User
        fields = ("email", "first_name", "last_name")

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                {
                    "password1": 'Os campos "Senha" e "Senha novamente" são diferentes',
                    "password2": 'Os campos "Senha" e "Senha novamente" são diferentes',
                }
            )

        email = cleaned_data.get("email")
        email2 = cleaned_data.get("email2")
        if email != email2:
            raise forms.ValidationError(
                {
                    "email": 'Os campos "Email" e "Email novamente" são diferentes',
                    "email2": 'Os campos "Email" e "Email novamente" são diferentes',
                }
            )

        return cleaned_data

    def save(self, commit=True) -> user_models.User:
        user: user_models.User.User = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class GondolaProductCreateForm(forms.ModelForm):
    class Meta:
        model = business_models.GondolaProduct
        fields = "__all__"


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = business_models.Product
        fields = ("barcode", "name")

    def save(self, commit=True) -> business_models.Product:
        return super().save(commit)
