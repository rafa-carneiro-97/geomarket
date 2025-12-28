from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path(
        "mapa/<int:establishment_id>/<uuid:locator_id>/",
        views.MapTemplateView.as_view(),
    ),
]
