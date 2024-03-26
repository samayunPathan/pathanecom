import json
import stripe
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category,Order,OrderItem
from .cart import Cart
from .forms import OrderForm

# for payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('store:cart_view')

def cart_view(request):
    cart=Cart(request)

    return render(request,'store/cart_view.html',{
        'cart':cart
    })

@login_required 
def checkout(request):
    cart=Cart(request)
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            total_price=0

            for item in cart:
                product=item['product']
                total_price+=product.price*int(item['quantity'])

            order=form.save(commit=False)
            order.created_by=request.user
            order.paid_amount=total_price
            order.save()
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()
            
            store_id='patha66018935391e5'
            API_key='patha66018935391e5@ssl'
            mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
            
            status_url=request.build_absolute_uri(reverse('store:complete'))

            total_amount=order.get_total_price()

            mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
            mypayment.set_product_integration(total_amount=Decimal(total_amount), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')

            mypayment.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')

            mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')
            response_data = mypayment.init_payment()

            return redirect(response_data['GatewayPageURL'])
    else:
        form=OrderForm()
    return render(request,'store/checkout.html',{
        'cart':cart,
        'form':form,
    })


    
@csrf_exempt
def complete(request):

    return render(request,'store/complete.html',context={})

def change_quantity(request,product_id):
    action=request.GET.get('action','')

    if action:
        quantity=1

        if action=='decrease':
            quantity=-1
        
        cart=Cart(request)
        cart.add(product_id,quantity,True)

    return redirect('store:cart_view')

def remove_from_cart(request,product_id):
    cart=Cart(request)
    cart.remove(product_id)

    return redirect('store:cart_view')

def search(request):
    query=request.GET.get('query','')
    products=Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query)|Q(description__icontains=query))

    return render(request,'store/search.html',{
        'query':query,
        'products':products,
    })

def product_details(request,category_slug, slug):
    product=get_object_or_404(Product,slug=slug,status=Product.ACTIVE)
    return render(request,'store/product_detail.html',{
        'product':product
    })

def category_detail(request,slug):
    category=get_object_or_404(Category,slug=slug)
    products=category.products.filter(status=Product.ACTIVE)
    return render(request,'store/category_detail.html',{
        'category':category,
        'products':products
    })

@csrf_exempt
def payment(request):
    order=get_object_or_404(Order)
    return render(request,'store/payment.html',{
        'order':order
    })