from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings

from users.forms import UserRegisterForm, UserLoginForm


class UserRegisterView(CreateView):
    """Регистрация пользователя"""

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        # Отправляем приветственное письмо
        send_mail(
            subject="Добро пожаловать в SkyStore!",
            message=f"Здравствуйте, {user.email}! Спасибо за регистрацию на нашем сайте.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        # Автоматически логиним пользователя
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    """Авторизация пользователя"""

    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("catalog:home")


class UserLogoutView(LogoutView):
    """Выход из системы"""

    next_page = reverse_lazy("catalog:home")  # type: ignore
