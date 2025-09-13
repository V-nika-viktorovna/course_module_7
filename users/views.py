import secrets

from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserForm, UserPasswordChangeForm, UserRegisterForm
from users.models import User


class UserRegisterView(CreateView):

    model = User
    template_name = "user_form.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):

        user = form.save()
        user.is_active = False
        token = secrets.token_hex(10)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/confirm-register/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserUpdateView(UpdateView):

    model = User
    template_name = "user_form.html"
    success_url = reverse_lazy("users:profile")
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):

    form_class = UserPasswordChangeForm
    template_name = "password_change_form.html"
    success_url = reverse_lazy("users:profile")
