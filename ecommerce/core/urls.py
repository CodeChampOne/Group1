from django.urls import path
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    ProductView,
    HomeView,
    OrderDetailsView,
    CheckoutView,
    PaymentView)
from django_countries.fields import CountryField


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<pk>/', ProductView.as_view(), name='product'),
    path('order-details', OrderDetailsView.as_view(), name='order-details'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', reduce_quantity_item, name='reduce-quantity-item'),
     path('checkout', CheckoutView.as_view(), name='checkout'),
     path('payment/<payment_option>/',
         PaymentView.as_view(), name='payment')
]