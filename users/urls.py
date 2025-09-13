from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import UserRegisterView, UserUpdateView, confirm_email

from . import views

app_name = UsersConfig.name


urlpatterns = [
    path("registration/", UserRegisterView.as_view(), name="registration"),

    path("users/login/", LoginView.as_view(template_name="login1.html"), name="login"),

    path("logout/", LogoutView.as_view(), name="logout"),

    path("confirm-register/<str:token>/", confirm_email, name="confirm_email"),

    path("profile/", UserUpdateView.as_view(), name="profile"),

    path("password-change/", views.UserPasswordChange.as_view(), name="password-change"),

    path("password-change/done/", PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
         name="password-change-done"),

    path("password-reset/", PasswordResetView.as_view(template_name="password_reset_form.html",
                                                      email_template_name="password_reset_email.html",
                                                      success_url=reverse_lazy("users:password_reset_done")),
         name="password_reset"),

    path("password-reset/done/", PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),

    path("password-reset/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",
                                          success_url=reverse_lazy("users:password_reset_complete")),
         name="password_reset_confirm"),

    path("password-reset/complete/",
         PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),
]
