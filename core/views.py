from django.shortcuts import render, HttpResponse
from .data import orders
from .models import Master, Review

def landing(request):
    masters = Master.objects.filter(is_active=True)[:6]  # Show first 6 active masters
    reviews = Review.objects.filter(is_published=True)[:6]  # Show first 6 published reviews
    context = {
        'masters': masters,
        'reviews': reviews,
    }
    return render(request, 'core/landing.html', context)

def thanks(request):
    return render(request, 'core/thanks.html')

def orders_list(request):
    context = {
        "orders": orders,  # Передаем список заказов в шаблон
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    # Используем next() для поиска первого совпадения
    order = next((order for order in orders if order["id"] == order_id), None)
    
    if order is None:
        return HttpResponse("<h1>Заказ не найден</h1>", status=404)
    
    context = {
        "order": order,
    }
    return render(request, "core/order_detail.html", context)




# Create your views here.
