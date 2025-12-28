from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("emissor/<uuid:id>/", consumers.InformationEmissorConsumer.as_asgi()),
    path("cart-locator/<uuid:id>/", consumers.CartLocatorConsumer.as_asgi()),
]
