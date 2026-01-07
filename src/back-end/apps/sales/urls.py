from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path(
        "mapa/<int:establishment_id>/<uuid:locator_id>/",
        views.MapTemplateView.as_view(),
        name="map",
    ),
    path(
        "mapa/<int:establishment_id>/<uuid:locator_id>/info",
        views.MapInfoView.as_view(),
        name="map-info",
    ),
]
