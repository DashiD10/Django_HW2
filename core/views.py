from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Master, Review, Order

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

@login_required
def orders_list(request):
    orders = Order.objects.all().order_by('-date_created')
    context = {
        "orders": orders,
    }
    return render(request, 'core/orders_list.html', context)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        "order": order,
    }
    return render(request, "core/order_detail.html", context)




# Create your views here.
