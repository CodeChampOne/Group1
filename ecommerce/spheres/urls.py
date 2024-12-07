from django.urls import path
from . import views

urlpatterns = [
    # Subscriber URLs
    path('subscribers/', views.subscriber_list, name='subscriber_list'),
    path('subscribers/<int:pk>/', views.subscriber_detail, name='subscriber_detail'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    # Payment URLs
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
]
