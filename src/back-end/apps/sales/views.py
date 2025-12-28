from django.views.generic.base import TemplateView


class MapTemplateView(TemplateView):
    template_name = "sales/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["establishment_id"] = self.kwargs["establishment_id"]
        context["locator_id"] = self.kwargs["locator_id"]
        return context
