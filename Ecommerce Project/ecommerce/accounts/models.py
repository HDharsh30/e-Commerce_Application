from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from home.models import Product

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def __str__(self):
        return f"User for {self.user.first_name}"

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        orderitems = self.cart_items.all()
        total = sum([item.get_total() for item in orderitems])
        return total
    
    def get_cart_quantity(self):
        orderitems = self.cart_items.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,blank=True)
    quantity = models.IntegerField(default=10)
    
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
User.cart = property(lambda u: Cart.objects.get_or_create(user=u)[0])

class ShippingAddress(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    landmark = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.address

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartItems, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} for {self.user.first_name}"


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try: 
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
        
    except Exception as e:
        print(e)
    
