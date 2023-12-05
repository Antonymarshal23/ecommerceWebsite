from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .utils import cartData, guestOrder

from django.contrib.auth import authenticate, login, logout

# show message in the forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserRegisterForm, CostomerForm

from .models import *

# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserRegisterForm()

        if request.method == 'POST':
            form = CreateUserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                user = authenticate(request, username=user.username, password=request.POST['password1'])

                if user is not None:
                    login(request, user)
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)
                    return redirect('login')

        context = {'form': form}
        return render(request, 'ecommerce/register.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            
            else:
                messages.info(request, 'Username Or Password Incorrect')

        return render(request, 'ecommerce/login.html')

def logoutUser(request):
    if request.user != None:
        logout(request)
    return redirect('store')

def store(request):
    if request.method == "GET":
        # advocate/?query=marshal
        query = request.GET.get('query')

        if query == None:
            query = ''
            
    product = Product.objects.filter(name__icontains=query)

    data = cartData(request)
    cartItems = data['cartItems']
    wishlistCount = data['wishlistCount']

    context = {'products': product, 'cartItems': cartItems, 'wishlistCount': wishlistCount,}

    return render(request, 'ecommerce/Store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    wishlistCount = data['wishlistCount']
            
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'wishlistCount': wishlistCount}
    return render(request, 'ecommerce/Cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    wishlistCount = data['wishlistCount']
    
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'wishlistCount': wishlistCount}
    return render(request, 'ecommerce/Checkout.html', context)

def view(request, name):
    product = Product.objects.get(name=name) 
    data = cartData(request)
    cartItems = data['cartItems']
    wishlistCount = data['wishlistCount']

    context = {"product": product, "cartItems": cartItems, 'wishlistCount': wishlistCount}
    return render(request, 'ecommerce/view.html', context)

@login_required(login_url='login')
def profile(request):
    page = "userInfo"

    data = cartData(request)
    cartItems = data['cartItems']
    customerDetails = data['customerDetails']
    wishlistCount = data['wishlistCount']

    context = {"cartItems": cartItems, "customerDetails": customerDetails, "page": page,'wishlistCount': wishlistCount}
    
    return render(request, 'ecommerce/profile.html', context)

@login_required(login_url='login')
def editUserInfo(request):
    page = "editUserInfo"

    customer = request.user.customer
    form = CostomerForm(instance=customer)

    
    if request.method == "POST":
        form = CostomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('profile')

    context = {"form": form, "page": page}
    return render(request, 'ecommerce/profile.html', context)

def add_to_wishlist(request):
    data = cartData(request)
    cartItems = data['cartItems']
    wishlists = data['wishlists']
    wishlistCount = data['wishlistCount']

    context = { "wishlists": wishlists, 'cartItems': cartItems, 'wishlistCount': wishlistCount}
    return render(request, 'ecommerce/wishlist.html', context)

def updateItem(request):
    # data parsing 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    
    # if the order avail get or create a new one 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)    
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

def updateWishList(request):
    # data parsing 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    user = request.user
    product = Product.objects.get(id=productId)
    
    # if the order avail get or create a new one 
    wishlist, created = Wishlist.objects.get_or_create(user=user, wished_item=product)

    if action == 'remove':
       wishlist.delete()


    return JsonResponse('item was added in the wishlist', safe=False)

def processOrder(request):  
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)

    else:
       customer, order = guestOrder(request, data)
       
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save() 
    

    if order.shipping == True: 
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],

        )

    return JsonResponse('payment submitted', safe=False)