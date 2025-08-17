from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import Master, Review, Order, Service
from .forms import ReviewForm, OrderForm, MasterServicesForm

def landing(request):
    masters = Master.objects.filter(is_active=True)[:6]  # Show first 6 active masters
    reviews = Review.objects.filter(is_published=True).select_related('master')[:6]  # Show first 6 published reviews with master info
    context = {
        'masters': masters,
        'reviews': reviews,
    }
    return render(request, 'core/landing.html', context)

def thanks(request):
    return render(request, 'core/thanks.html')

@login_required
def orders_list(request):
    orders = Order.objects.all().select_related('master').prefetch_related('master__services').order_by('-date_created')
    
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
    order = get_object_or_404(
        Order.objects.select_related('master').prefetch_related('master__services').annotate(
            total_price=Sum('master__services__price')
        ), 
        pk=pk
    )
    context = {
        "order": order,
    }
    return render(request, "core/order_detail.html", context)

def create_review(request):
    """Форма создания отзыва"""
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'title': 'Оставить отзыв'
    }
    return render(request, 'core/create_review.html', context)

def create_order(request):
    """Форма создания заявки"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = OrderForm()
    
    context = {
        'form': form,
        'title': 'Записаться на услугу'
    }
    return render(request, 'core/create_order.html', context)

def get_master_services(request):
    """API endpoint для получения услуг мастера (AJAX)"""
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        master_id = request.GET.get('master_id')
        if master_id:
            try:
                master = Master.objects.get(id=master_id)
                services = master.services.all()
                services_data = [{
                    'id': service.id,
                    'name': service.name,
                    'price': str(service.price),
                    'duration': service.duration
                } for service in services]
                return JsonResponse({'services': services_data})
            except Master.DoesNotExist:
                return JsonResponse({'error': 'Master not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Create your views here.
