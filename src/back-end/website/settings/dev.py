from .default import *
from django.urls import reverse_lazy


INSTALLED_APPS += [
    "debug_toolbar",
]


MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


INTERNAL_IPS = [
    "127.0.0.1",
]

# URLS that TOOLBAR will ignore
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: not any(
        str(path) in request.path for path in [reverse_lazy("spa:index")]
    ),
}
