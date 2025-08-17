from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Order, Master, Service, Review, SiteSettings

# Custom filters
class AppointmentDateFilter(admin.SimpleListFilter):
    title = 'Дата записи'
    parameter_name = 'appointment_date_filter'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Сегодня'),
            ('tomorrow', 'Завтра'),
            ('this_week', 'На этой неделе'),
        ]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        
        if self.value() == 'today':
            return queryset.filter(appointment_date__date=today)
        elif self.value() == 'tomorrow':
            tomorrow = today + timedelta(days=1)
            return queryset.filter(appointment_date__date=tomorrow)
        elif self.value() == 'this_week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(
                appointment_date__date__gte=start_of_week,
                appointment_date__date__lte=end_of_week
            )
        return queryset

# Inline classes
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['client_name', 'rating', 'text', 'created_at']
    fields = ['client_name', 'rating', 'text', 'created_at', 'is_published']

# Custom actions for Order
@admin.action(description='Подтвердить выбранные заказы')
def confirm_orders(modeladmin, request, queryset):
    queryset.update(status='confirmed')

@admin.action(description='Отменить выбранные заказы')
def cancel_orders(modeladmin, request, queryset):
    queryset.update(status='canceled')

@admin.action(description='В работе выбранные заказы')
def in_progress_orders(modeladmin, request, queryset):
    queryset.update(status='in_progress')

@admin.action(description='Завершить выбранные заказы')
def complete_orders(modeladmin, request, queryset):
    queryset.update(status='completed')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'phone', 'master', 'status', 'appointment_date', 'total_price', 'date_created']
    list_filter = ['status', 'master', AppointmentDateFilter]
    search_fields = ['name', 'phone']
    list_editable = ['status']
    actions = [confirm_orders, cancel_orders, in_progress_orders, complete_orders]
    date_hierarchy = 'appointment_date'
    list_per_page = 20
    
    def client_name(self, obj):
        return obj.name
    client_name.short_description = 'Имя клиента'
    
    def total_price(self, obj):
        # Since there's no direct Order-Service relationship, we'll show a placeholder
        # In a real scenario, you might have an OrderService intermediate model
        return "Услуги через мастера"
    total_price.short_description = 'Общая стоимость'

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'experience', 'is_active', 'service_count']
    list_filter = ['is_active', 'services']
    search_fields = ['name']
    filter_horizontal = ['services']
    list_per_page = 20
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Кол-во услуг'
    
    inlines = [ReviewInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_popular']
    list_filter = ['is_popular']
    search_fields = ['name']
    list_per_page = 20

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'master', 'rating', 'created_at', 'is_published']
    list_filter = ['rating', 'is_published', 'created_at']
    search_fields = ['client_name', 'text']
    list_per_page = 20

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone']
