from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("login/form", views.LoginView.as_view()),
    path("auth/token/validate", views.ValidateToken.as_view()),
    path("auth/user/info", views.UserInfoView.as_view()),
    path("auth/user/permissions", views.PermissionsView.as_view()),
]
