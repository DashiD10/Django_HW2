from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import get_user_model

from .forms import (
    UserLoginForm, UserRegisterForm, UserProfileUpdateForm,
    UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
)
from .models import UserProfile

User = get_user_model()


class UserRegisterView(CreateView):
    """Представление регистрации пользователя"""
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('core:landing')
    
    def dispatch(self, request, *args, **kwargs):
        """Защита от доступа аутентифицированных пользователей"""
        if request.user.is_authenticated:
            messages.info(request, 'Вы уже зарегистрированы и вошли в систему.')
            return redirect('core:landing')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Автоматический вход после регистрации"""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация прошла успешно! Добро пожаловать!')
        return response
    
    def form_invalid(self, form):
        """Обработка ошибок формы"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """Представление входа пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Обработка параметра next для перенаправления"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('core:landing')
    
    def form_valid(self, form):
        """Успешный вход"""
        messages.success(self.request, f'Добро пожаловать, {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Ошибка входа"""
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    """Представление выхода пользователя"""
    next_page = reverse_lazy('core:landing')
    
    def dispatch(self, request, *args, **kwargs):
        """Добавление сообщения об успешном выходе"""
        if request.user.is_authenticated:
            messages.success(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """Представление детального просмотра профиля"""
    model = UserProfile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        """Получение профиля по ID пользователя"""
        user_id = self.kwargs.get('pk')
        return get_object_or_404(UserProfile, user_id=user_id)
    
    def get_context_data(self, **kwargs):
        """Добавление проверки принадлежности профиля"""
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object.user
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление обновления профиля"""
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update_form.html'
    
    def get_object(self, queryset=None):
        """Получение только собственного профиля"""
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def get_success_url(self):
        """URL после успешного обновления"""
        return reverse_lazy('users:profile_detail', kwargs={'pk': self.request.user.pk})
    
    def form_valid(self, form):
        """Успешное обновление"""
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Ошибка обновления"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Представление смены пароля"""
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:profile_detail')
    
    def get_success_url(self):
        """URL после успешной смены пароля"""
        return reverse_lazy('users:profile_detail', kwargs={'pk': self.request.user.pk})
    
    def form_valid(self, form):
        """Успешная смена пароля"""
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    """Представление запроса восстановления пароля"""
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Представление подтверждения отправки email"""
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Представление подтверждения сброса пароля"""
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Представление завершения сброса пароля"""
    template_name = 'users/password_reset_complete.html'
