from django.contrib import admin
from .models import Subscriber, Administrator, Product, Order, OrderDetails, Payment

admin.site.register(Subscriber)
admin.site.register(Administrator)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Payment)
