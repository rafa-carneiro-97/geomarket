from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from .jwt import authenticate_jwt_header


class ValidateJWTHeaderMixin(LoginRequiredMixin):
    """Verify that the current JWT header is valid."""

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        try:
            authenticate_jwt_header(request)
        except ValueError as e:
            return http.JsonResponse({"error": str(e)}, status=401)
        return super().dispatch(request, *args, **kwargs)
