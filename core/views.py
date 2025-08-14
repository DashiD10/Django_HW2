from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    
    # Get search query and checkbox values from GET request
    search_query = request.GET.get('q', '')
    search_name = request.GET.get('search_name', '')  # Default empty means unchecked
    search_phone = request.GET.get('search_phone', '')
    search_comment = request.GET.get('search_comment', '')
    
    # Build Q objects based on selected checkboxes
    if search_query:
        q_objects = Q()
        
        if search_name:
            q_objects |= Q(name__icontains=search_query)
        if search_phone:
            q_objects |= Q(phone__icontains=search_query)
        if search_comment:
            q_objects |= Q(comment__icontains=search_query)
        
        # If no checkboxes are selected, default to search by name
        if not any([search_name, search_phone, search_comment]):
            q_objects = Q(name__icontains=search_query)
        
        orders = orders.filter(q_objects)
    
    context = {
        "orders": orders,
        "search_query": search_query,
        "search_name": search_name,
        "search_phone": search_phone,
        "search_comment": search_comment,
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
