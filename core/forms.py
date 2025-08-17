from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Review, Order, Master, Service

class ReviewForm(ModelForm):
    """Форма создания отзыва"""
    
    RATING_CHOICES = [
        (1, '1 звезда - Ужасно'),
        (2, '2 звезды - Плохо'),
        (3, '3 звезды - Удовлетворительно'),
        (4, '4 звезды - Хорошо'),
        (5, '5 звезд - Отлично'),
    ]
    
    master = forms.ModelChoiceField(
        queryset=Master.objects.filter(is_active=True),
        empty_label="Выберите мастера",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    client_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя (необязательно)'
        })
    )
    
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Поделитесь вашим опытом...'
        })
    )
    
    class Meta:
        model = Review
        fields = ['master', 'rating', 'client_name', 'text']
        labels = {
            'master': 'Мастер',
            'rating': 'Оценка',
            'client_name': 'Имя клиента',
            'text': 'Отзыв'
        }


class OrderForm(ModelForm):
    """Форма создания заявки"""
    
    master = forms.ModelChoiceField(
        queryset=Master.objects.filter(is_active=True),
        empty_label="Выберите мастера",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_master'})
    )
    
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        })
    )
    
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Комментарий (необязательно)'
        })
    )
    
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
    
    class Meta:
        model = Order
        fields = ['master', 'services', 'name', 'phone', 'comment', 'appointment_date']
        labels = {
            'master': 'Мастер',
            'services': 'Услуги',
            'name': 'Имя клиента',
            'phone': 'Телефон',
            'comment': 'Комментарий',
            'appointment_date': 'Дата и время записи'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если мастер уже выбран, ограничиваем список услуг
        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['services'].queryset = Service.objects.filter(
                    masters__id=master_id
                )
            except (ValueError, TypeError):
                self.fields['services'].queryset = Service.objects.none()
        elif self.instance.pk:
            # Для редактирования существующего заказа
            self.fields['services'].queryset = self.instance.master.services.all()
    
    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')
        
        if master and services:
            # Проверяем, что все выбранные услуги предоставляются мастером
            master_services = master.services.all()
            invalid_services = []
            
            for service in services:
                if service not in master_services:
                    invalid_services.append(service.name)
            
            if invalid_services:
                raise forms.ValidationError(
                    f"Мастер {master.name} не предоставляет услуги: {', '.join(invalid_services)}"
                )
        
        return cleaned_data


# Форма для AJAX запросов (опционально)
class MasterServicesForm(forms.Form):
    """Форма для получения услуг конкретного мастера"""
    master_id = forms.IntegerField()
    
    def get_services(self):
        master_id = self.cleaned_data['master_id']
        return Service.objects.filter(masters__id=master_id)
