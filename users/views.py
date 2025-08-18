from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    """Классовое представление для входа пользователя"""
    form_class = UserLoginForm
    template_name = 'users/form.html'
    
    def get_context_data(self, **kwargs):
        """Добавляем заголовок и текст кнопки в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        context['button_text'] = 'Войти'
        return context


class UserRegistrationView(CreateView):
    """Классовое представление для регистрации пользователя"""
    form_class = UserRegistrationForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        """Добавляем заголовок и текст кнопки в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['button_text'] = 'Зарегистрироваться'
        return context


class UserLogoutView(LogoutView):
    """Классовое представление для выхода пользователя"""
    next_page = reverse_lazy('login')
