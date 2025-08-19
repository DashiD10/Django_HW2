from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        })
        
        # Убираем help_text
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserProfileUpdateForm(forms.ModelForm):
    """Форма обновления профиля пользователя"""
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'birth_date', 'telegram_id', 'github_id']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telegram_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telegram ID'
            }),
            'github_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GitHub ID'
            }),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    """Форма смены пароля пользователя"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Старый пароль'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтверждение нового пароля'
        })
        
        # Убираем help_text
        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None


class CustomPasswordResetForm(PasswordResetForm):
    """Форма запроса восстановления пароля"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'
        })


class CustomSetPasswordForm(SetPasswordForm):
    """Форма установки нового пароля"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтверждение нового пароля'
        })
        
        # Убираем help_text
        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None
