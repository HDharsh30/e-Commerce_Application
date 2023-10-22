from django.urls import path
from .views import *
from accounts.views import login_page

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_page, name="login"),
    path('myprofile/', my_profile, name="myprofile"),
    path('product/', product, name="product"),
    path('by-now/<slug>', by_now, name = "by-now"),
    path('view-cart/', view_cart, name="view_cart"),
    path('product/<slug>', product_detail, name="product-deatil"),
    path('add-to-cart/<slug>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', remove_from_cart, name="remove-from-cart"),
    path('increase-cart-item/<slug>', increase_cart_item, name="increase-cart-item"),
    path('decrese-cart-item/<slug>', decrease_cart_item, name="decrease-cart-item"),
    path('place_order', place_order, name='place_order'),
    path('order_confirmation/', order_confirmation, name='order_confirmation'),
    path('contact', contact, name="contact"),
]
