from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("admin/login/", lambda request: redirect(settings.LOGIN_URL)),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.users.urls")),
    path("", include("apps.business.urls")),
    path("api/", include("apps.api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(path("", include("apps.spa.urls")))  # this must be the last)


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
