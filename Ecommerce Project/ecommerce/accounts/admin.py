from django.contrib import admin
from .models import Profile, Cart, CartItems, ShippingAddress, Order

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(ShippingAddress)
admin.site.register(Order)