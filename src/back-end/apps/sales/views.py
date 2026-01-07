from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView
from apps.users.models import User


class MapTemplateView(TemplateView):
    template_name = "sales/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["establishment_id"] = self.kwargs["establishment_id"]
        context["locator_id"] = self.kwargs["locator_id"]
        return context


class MapInfoView(UserPassesTestMixin, TemplateView):
    template_name = "sales/map-info.html"

    def test_func(self):
        user: User = self.request.user

        if not user.is_authenticated:
            return False

        if not user.is_active:
            return False

        if not self.request.user.is_staff:
            return False

        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["establishment_id"] = self.kwargs["establishment_id"]
        context["locator_id"] = self.kwargs["locator_id"]
        return context
