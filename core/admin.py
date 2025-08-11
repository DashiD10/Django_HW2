from django.contrib import admin
from .models import Order, Master, Service, Review, SiteSettings

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'status', 'master', 'appointment_date', 'date_created']
    list_filter = ['status', 'date_created', 'master']
    search_fields = ['name', 'phone']
    date_hierarchy = 'date_created'

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'experience', 'is_active']
    list_filter = ['is_active', 'experience']
    search_fields = ['name', 'phone']
    filter_horizontal = ['services']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_popular']
    list_filter = ['is_popular']
    search_fields = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'master', 'rating', 'created_at', 'is_published']
    list_filter = ['rating', 'is_published', 'created_at']
    search_fields = ['client_name', 'text']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone']
