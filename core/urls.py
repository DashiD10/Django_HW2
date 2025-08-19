from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('create-review/', views.ReviewCreateView.as_view(), name='create_review'),
    path('create-order/', views.OrderCreateView.as_view(), name='create_order'),
    
    # API endpoint for AJAX requests
    path('get-master-services/', views.get_master_services, name='get_master_services'),
]
