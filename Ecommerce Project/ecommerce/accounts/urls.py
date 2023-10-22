from django.urls import path
from .views import *
from home.views import add_to_cart

urlpatterns = [
    path('login/', login_page, name="login"),
    path('signup/', signup, name="signup"),
    path('guest-user', guest_user, name="guest-user"),
    path('activate/<email_token>', activate_email,name="activate_email"),
    #path('cart/', cart, name = "cart"),
    path('add_to_cart/<slug>/', add_to_cart, name="add_to_cart"),
    path('logout', logout_user, name="logout")
]