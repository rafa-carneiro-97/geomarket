from django import http
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from .jwt import authenticate_jwt_header
from apps.users import models as users_models
from apps.business import models as business_models


class ValidateJWTHeaderMixin(LoginRequiredMixin):
    """Verify that the current JWT header is valid."""

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        try:
            authenticate_jwt_header(request)
        except ValueError as error:
            return http.JsonResponse({"error": str(error)}, status=401)
        return super().dispatch(request, *args, **kwargs)


class EstablishmentAccessMixin(AccessMixin):
    """
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    permission_denied_message = "Permissão negada"
    redirect_field_name = None
    raise_exception = False
    establishment_id_kwargs = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.has_permission():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def has_permission(self) -> bool:
        employee = self.get_employee_object()
        if employee is not None:
            return True

        return False

    def get_establishment_id(self) -> int:
        establishment_id = self.kwargs.get(self.establishment_id_kwargs)

        if not establishment_id:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the establishment_id_kwargs attribute. Define {self.__class__.__name__}.establishment_id_kwargs."
            )

        return establishment_id

    def get_employee_queryset(self) -> business_models.EstablishmentEmployee:
        return business_models.EstablishmentEmployee.objects.select_related(
            "establishment",
        ).filter(user=self.request.user, establishment__is_active=True)

    def get_employee_object(self) -> business_models.EstablishmentEmployee:
        user: users_models.User = self.request.user
        establishment_id = self.get_establishment_id()

        cache_key = f"api:employee_{user.id}_{establishment_id}"
        establishment = cache.get(cache_key)

        if establishment is not None:
            return establishment

        if user.is_staff:
            return self._generate_temporary_employee(user)

        try:
            obj = self.get_employee_queryset().get(establishment__id=establishment_id)
            cache.set(cache_key, obj, timeout=10 * 60)  # 10 minutes
            return obj
        except ObjectDoesNotExist:
            raise http.Http404("Employee not found.")

    def _generate_temporary_employee(
        self, user: users_models.User
    ) -> business_models.EstablishmentEmployee | None:
        if not user.is_staff:
            raise Exception(
                "Can not create a temporary employee for user who are not staff."
            )

        establishment = business_models.Establishment.objects.filter(
            id=self.get_establishment_id()
        ).first()

        if not establishment:
            raise http.Http404("Establishment not found.")

        temporary_employee = business_models.EstablishmentEmployee()
        temporary_employee.user = user
        temporary_employee.is_admin = True
        temporary_employee.establishment = establishment

        return temporary_employee
