from django.shortcuts import render, HttpResponse
from .data import orders

def landing(request):
    return render(request, 'core/landing.html')

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
