import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack

from website.urls import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        # Prefix all websocket routes with /ws/
                        path("ws/", URLRouter(websocket_urlpatterns)),
                    ]
                )
            )
        ),
    }
)
