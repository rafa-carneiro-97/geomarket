from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("login/form", views.LoginFormView.as_view()),
    path("user/form/create", views.UserCreateView.as_view()),
    path("email/verification/send", views.EmailVerificationSendView.as_view()),
    path("email/verify", views.EmailVerifyView.as_view()),
    path("auth/token/validate", views.ValidateToken.as_view()),
    path("auth/user/info", views.UserInfoView.as_view()),
    path("establishments/list", views.EstablishmentsListDataView.as_view()),
    path(
        "establishment/<int:establishment_id>/",
        views.EstablishmentDataView.as_view(),
    ),
    path(
        "establishment/<int:establishment_id>/dashboard",
        views.DashboardDataView.as_view(),
    ),
    path(
        "establishment/<int:establishment_id>/product/create",
        views.EstablishmentProductCreateView.as_view(),
    ),
]
