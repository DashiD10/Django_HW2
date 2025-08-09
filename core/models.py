from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='BRUTAL Barbershop')
    phone = models.CharField(max_length=20, default='+7 (999) 123-45-67')
    
    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

# <!-- Используем в любом шаблоне -->
# <footer>
#   <p>{{ site_name }} — звоните: {{ phone }}</p>
# </footer>

