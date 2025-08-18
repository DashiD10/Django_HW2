from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    """Кастомная форма аутентификации пользователя"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control из Bootstrap 5 ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegistrationForm(UserCreationForm):
    """Кастомная форма регистрации пользователя"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control из Bootstrap 5 ко всем полям
        for field_name, field in self.fields.items():
            if field_name != 'email':  # email уже имеет form-control в Meta
                field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        """Валидация email на уникальность"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email
