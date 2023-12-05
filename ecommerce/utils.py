import json
from django.contrib import messages

from .models import *

def cookiesCart(request):
    try: 
        cart = json.loads(request.COOKIES['cart'])
        wishlist = json.loads(request.COOKIES['wishlist'])
    except:
        cart={}
        wishlist = []

     # for cart items
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    wish = []

    # for wishlist items
    numOfWishList = {'get_wishlist_items': 0}
    wishlistItem = numOfWishList['get_wishlist_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            
            product = Product.objects.get(id=i)

            total = (product.price * cart[i]["quantity"]) 

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    'id': product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity': cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True 
        except:
            pass
    
    for i in wishlist:
        try:
            wishlistItem += wishlist[i]["quantity"]
            product = Product.objects.get(id=i)
            item = {
                'wished_item':{
                    'id': product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                }
            }
            wish.append(item)
        except:
            pass

    return{'cartItems': cartItems, 'order': order, 'items': items, 'wish': wish, 'wishlistItem': wishlistItem}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        user = request.user

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        customerDetails = Customer.objects.filter(user=user)

        wishlists = Wishlist.objects.filter(user=user)
        wishlistCount = wishlists.count()
    else:
        cookiesData = cookiesCart(request)
        cartItems = cookiesData['cartItems']
        order = cookiesData['order']
        items = cookiesData['items']
        wishlists = cookiesData['wish']

        customerDetails = []

        wishlistCount = cookiesData['wishlistItem']
    return {'cartItems': cartItems, 'order':order, 'items': items, 'customerDetails': customerDetails, 'wishlists': wishlists, 'wishlistCount':wishlistCount}


def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	# get the items in the cart page. so we have to use cookieCart.
	# cookieCart get the toal item in the cart page 
	cookieData = cookiesCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	# just for if the customer want to add new name with the same email id.
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['product']['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return (customer, order)