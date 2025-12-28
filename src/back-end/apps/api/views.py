import logging, hashlib
from django import http
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.cache import cache
from django.template import loader
from django.views import View
from django.views.generic.edit import CreateView
from apps.users.models import User
from apps.business import models as business_models
from apps.sales import models as sales_models
from .jwt import generate_jwt_token
from . import forms, mixins


def hash_user_email(user: User):
    sha256_hash = hashlib.sha256(user.email.encode()).hexdigest()
    data = ""

    for item in range(6):
        number = int(sha256_hash[item], 16)
        data += f"{number}"

    return data[:6]


class LoginFormView(AuthLoginView):
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


class UserCreateView(CreateView):
    form_class = forms.CustomUserCreationForm

    def form_valid(self, form: forms.CustomUserCreationForm):
        form.save()
        return http.HttpResponse(status=201)

    def form_invalid(self, form: forms.CustomUserCreationForm):
        return http.JsonResponse({"errors": form.errors}, status=400)


class EmailVerificationSendView(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        user: User = self.request.user
        if user.is_email_verified:
            return http.HttpResponse(status=409)

        cache_key = f"api:email-verification:counter:user-{user.email}"
        counter = cache.get(cache_key, 0)

        if counter >= 5:
            return http.HttpResponse(status=204)

        cache.set(cache_key, counter + 1, timeout=24 * 60 * 60)  # 24 hours
        self._send_verification_email()

        return http.HttpResponse(status=200)

    def _send_verification_email(self):
        user: User = self.request.user
        html_message = self._generate_email_message()

        try:
            user.send_email(subject="Verificação de email", html_message=html_message)
        except Exception as exception:
            logging.error(
                f"Error on sending verification email to user ({user.id}): {str(exception)}"
            )

    def _generate_email_message(self) -> str:
        code = hash_user_email(user=self.request.user)

        return loader.render_to_string(
            template_name="api/email/verification.html",
            request=self.request,
            context={
                "code": code,
            },
        )


class EmailVerifyView(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["post"]

    def post(self, *args, **kwargs) -> http.HttpResponse:
        user: User = self.request.user
        code = self.request.POST.get("code", "")
        hashed_code = hash_user_email(user=self.request.user)

        if code != hashed_code:
            return http.HttpResponse(status=209)

        user.is_email_verified = True
        user.save()
        return http.HttpResponse(status=200)


class ValidateToken(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        return http.HttpResponse(status=204)


class UserInfoView(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        user: User = self.request.user
        data = {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "isStaff": user.is_staff,
            "isEmailVerified": user.is_email_verified,
        }
        return http.JsonResponse(data=data, status=200)


class EstablishmentsListDataView(mixins.ValidateJWTHeaderMixin, View):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        employees = business_models.Employee.objects.select_related(
            "establishment"
        ).filter(user=self.request.user, establishment__is_active=True)
        data = []

        for item in employees:
            data.append({"id": item.establishment.id, "name": item.establishment.name})

        return http.JsonResponse(data=data, safe=False, status=200)


class EstablishmentDataView(
    mixins.ValidateJWTHeaderMixin,
    mixins.EstablishmentAccessMixin,
    View,
):
    http_method_names = ["get"]
    establishment_id_kwargs = "establishment_id"

    def get(self, *args, **kwargs) -> http.HttpResponse:
        employee = self.get_employee_object()

        data = {
            "name": employee.establishment.name,
            "address": employee.establishment.address,
        }

        return http.JsonResponse(data=data, safe=False, status=200)


class DashboardDataView(
    mixins.ValidateJWTHeaderMixin,
    mixins.EstablishmentAccessMixin,
    View,
):
    http_method_names = ["get"]
    establishment_id_kwargs = "establishment_id"

    def get(self, *args, **kwargs) -> http.HttpResponse:
        data = {}

        employee = self.get_employee_object()

        has_any_employee_perm = employee.has_any_perms(
            ["view_employee", "add_employee", "delete_employee", "change_employee"]
        )

        if has_any_employee_perm:
            employees_queryset = business_models.Employee.objects.filter(
                establishment=employee.establishment
            )
            data["employee"] = {
                "admin": employees_queryset.filter(is_admin=True).count(),
                "usual": employees_queryset.filter(is_admin=False).count(),
            }

        return http.JsonResponse(data=data, safe=False, status=200)


class GondolaProductsDataView(
    mixins.ValidateJWTHeaderMixin,
    mixins.EstablishmentAccessMixin,
    View,
):
    http_method_names = ["get"]
    establishment_id_kwargs = "establishment_id"

    def get(self, *args, **kwargs) -> http.HttpResponse:
        gondola_products = (
            sales_models.GondolaProduct.objects.select_related("product")
            .prefetch_related("product__keywords")
            .filter(
                gondola__id=kwargs.get("gondola_id"),
                gondola__establishment__id=self.get_establishment_id(),
            )
        )

        data = []

        for item in gondola_products:
            keywords = list(
                item.product.keywords.all().values_list("keyword", flat=True)
            )

            if item.product.photo and hasattr(item.product.photo, "url"):
                photo_url = item.product.photo.url
            else:
                photo_url = None

            data.append(
                {
                    "id": item.id,
                    "gondola": {
                        "xPosition": item.gondola_x_position,
                        "yPosition": item.gondola_y_position,
                    },
                    "product": {
                        "id": item.product.id,
                        "name": item.product.name,
                        "codebar": item.product.barcode,
                        "keywords": keywords,
                        "photoUrl": photo_url,
                        "isActive": item.product.is_active,
                    },
                }
            )

        return http.JsonResponse(data=data, safe=False, status=200)


class ProductsDataView(
    mixins.ValidateJWTHeaderMixin,
    View,
):
    http_method_names = ["get"]

    def get(self, *args, **kwargs) -> http.HttpResponse:
        barcode = kwargs.get("barcode")

        if not barcode:
            raise http.Http404()

        try:
            product = business_models.Product.objects.prefetch_related("keywords").get(
                barcode=barcode
            )

            keywords = list(product.keywords.all().values_list("keyword", flat=True))

            if product.photo and hasattr(product.photo, "url"):
                photo_url = product.photo.url
            else:
                photo_url = None

            data = data = {
                "id": product.id,
                "name": product.name,
                "barcode": product.barcode,
                "photoUrl": photo_url,
                "keywords": keywords,
                "isActive": product.is_active,
            }

            return http.JsonResponse(data, safe=False, status=200)

        except business_models.Product.DoesNotExist:
            return http.HttpResponse(status=204)


class ProductsCreateView(mixins.ValidateJWTHeaderMixin, CreateView):
    model = business_models.Product
    form_class = forms.ProductCreateForm

    def form_valid(self, form: forms.ProductCreateForm):
        obj = form.save()
        logging.info(f'Successfully created the product "{obj.name} #{obj.barcode}".')
        data = {
            "id": obj.id,
            "name": obj.name,
            "barcode": obj.barcode,
            "kewords": [],
            "photoUrl": None,
            "isActive": obj.is_active,
        }
        return http.JsonResponse(data=data, status=201)

    def form_invalid(self, form: forms.ProductCreateForm):
        name = form.cleaned_data.get("name", "-")
        barcode = form.cleaned_data.get("barcode", "-")
        logging.info(f'Failed on creating the product "{name} #{barcode}".')
        return http.JsonResponse({"errors": form.errors}, status=400)


class EstablishmentMapDataView(View):
    http_method_names = ["get"]

    def dispatch(self, request, *args, **kwargs):
        self.establishment_id = kwargs.get("establishment_id")
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs) -> http.HttpResponse:
        sales_map = self.queryset()

        if sales_map:
            data = sales_map.map
        else:
            data = {}

        return http.JsonResponse(data=data, safe=False, status=200)

    def queryset(self) -> sales_models.SalesMap | None:
        key = f"api:establishment-map:establishment-{self.establishment_id}"
        cached_map = cache.get(key)

        if cached_map is not None:
            return cached_map

        map = sales_models.SalesMap.objects.filter(
            establishment=self.establishment_id
        ).first()

        cache.set(key, map, timeout=600)  # 10 minutes

        return map
