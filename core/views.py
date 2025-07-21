from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')

def thanks(request):
    return render(request, 'thanks.html')

def orders_list(request):
    return render(request, 'orders_list.html')

def order_detail(request, order_id):
    return render(request, 'order_detail.html')



# Create your views here.
