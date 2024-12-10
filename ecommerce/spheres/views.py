from django.shortcuts import render, get_object_or_404
from .models import Subscriber, Administrator, Product, Order, OrderDetails, Payment
from django.http import HttpResponse


def product_list(request):
    products = Product.objects.all()
    return render(request, 'spheres/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'spheres/product_detail.html', {'product': product})


def subscriber_list(request):
    subscribers = Subscriber.objects.all()
    return render(request, 'spheres/subscriber_list.html', {'subscribers': subscribers})


def subscriber_detail(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    return render(request, 'spheres/subscriber_detail.html', {'subscriber': subscriber})


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'spheres/order_list.html', {'orders': orders})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'spheres/order_detail.html', {'order': order})

def payment_list(request):
    orders = Order.objects.all()
    return render(request, 'spheres/payment_list.html', {'payments': orders})


def payment_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'spheres/payment_detail.html', {'payment': order})