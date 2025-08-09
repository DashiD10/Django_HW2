from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {
        'site_name': settings.site_name if settings else 'BRUTAL Barbershop',
        'phone': settings.phone if settings else '+7 (999) 123-45-67',
    }

