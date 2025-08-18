"""
URL configuration for barbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('review/create/', views.create_review, name='create_review'),
    path('orders/create/', views.create_order, name='create_order'),
    path('api/master-services/', views.get_master_services, name='get_master_services'),
    path('users/', include('users.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
