from django import http
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.views import View
from apps.users.models import User
from apps.business import models as business_models
from .jwt import generate_jwt_token
from . import forms, mixins


class LoginView(AuthLoginView):
    http_method_names = ["post"]
    form_class = forms.CustomAuthenticationForm

    def form_valid(self, form: forms.CustomAuthenticationForm):
        user: User = form.get_user()
        login(self.request, user)

        if not form.cleaned_data["stay_connected"]:
            self.request.session.set_expiry(0)

        token = generate_jwt_token(self.request, user)

        return http.JsonResponse(data={"token": token}, status=200)

    def form_invalid(self, form: forms.CustomAuthenticationForm):
        return http.JsonResponse({"errors": form.errors}, status=400)


class ValidateToken(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        return http.HttpRequest(data="ok", status=200)


class UserInfoView(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        user: User = self.request.user
        data = {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "isStaff": user.is_staff,
        }
        return http.JsonResponse(data=data, status=200)


class PermissionsView(View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        employee = business_models.Employee.objects.all().first()

        return http.HttpResponse(employee.has_perm(codename="add_employee"))
