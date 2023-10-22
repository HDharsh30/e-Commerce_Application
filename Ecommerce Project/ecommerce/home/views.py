from django.shortcuts import render, redirect
from .models import *
from accounts.models import Cart, CartItems, Order, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    context = {'products':Product.objects.all()}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def my_profile(request):
    username = request.user.username
    context = {"user_person":username}
    return render(request, 'myprofile.html', context)

def product(request):
    context = {'products':Product.objects.all()}
    return render(request, 'product.html', context)

def product_detail(request, slug):
    try:
        product = Product.objects.get(slug =slug)
        context={'product':product}
        return render(request, 'product_detail.html',context=context)
    
    except Exception as e:
        print(e)

@login_required(login_url='login')
def by_now(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user
    cart, created = Cart.objects.get_or_create(user = request.user)
    
    cart_items, item_created = CartItems.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_items.quantity += 10
        cart_items.save()
    return redirect('view_cart')

@login_required(login_url='login')
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItems.objects.filter(cart=cart)
    cart = Cart.objects.get(user=request.user)
    cart_total = cart.get_cart_total()
    quantity_total = cart.get_cart_quantity()
    return render(request, 'checkout.html', {'cart_item': cart_items, 'cart_total': cart_total, 'quantity_total':quantity_total})

@login_required(login_url='login')
def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItems.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 10
        
    cart_item.save()
    messages.warning(request, "Thank You! Product is added to cart.")
    return redirect('product')

@login_required(login_url='login')
def remove_from_cart(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        cart = Cart.objects.get(user=request.user)
        
        try:
            cart_item = CartItems.objects.get(cart=cart, product=product)
            if cart_item.quantity > 1:
                cart_item.delete()
        except CartItems.DoesNotExist:
            pass
        
    except (Product.DoesNotExist, Cart.DoesNotExist) as e:
        print(e)

    return redirect('view_cart')

@login_required(login_url='login')
def increase_cart_item(request, slug):
    product = Product.objects.get(slug=slug)
    cart = request.user.cart
    
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1

    cart_item.save()
    return redirect('view_cart')

@login_required(login_url='login')
def decrease_cart_item(request, slug):
    product = Product.objects.get(slug=slug)
    cart = request.user.cart
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)

    if cart_item.quantity > 10:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')

@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        address = request.POST.get("address")
        landmark = request.POST.get("landmark")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pin_code = request.POST.get("zip")
        
        user = request.user
        cart = user.cart

        shipping_address = ShippingAddress(
            user=user.profile,
            order=cart,
            address=address,
            landmark=landmark,
            city=city,
            state=state,
            zipcode=pin_code
        )
        shipping_address.save()

        total_price = cart.get_cart_total()
        order_item = cart.cart_items.first()

        order = Order.objects.create(
            user=user,
            cart=cart,
            order_item=order_item,
            shipping_address=shipping_address,
            total_amount=total_price,
        )

        cart.is_paid = True
        cart.save()

        return redirect('order_confirmation')

    return redirect('view_cart')

def order_confirmation(request):
    return render(request, 'complete_order.html')


@login_required(login_url='login')
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        myquery = Contact_us(user_name=name, email=email, subject=subject, user_message=message)
        myquery.save()
        messages.warning(request, "Thank You! We will contact you shortly…")
        return redirect('contact')
    
    return render(request, 'contact.html')
