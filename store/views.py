
import email
from itertools import product
from multiprocessing import context
from tokenize import Number
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import datetime
from .utils import cookieCart, guestOrder


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:

        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def category(request, category):
    product = Product.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "product": product
    }
    return render(request, "category.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
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
    return JsonResponse('Form Submitted!', safe=False)
#search Bar
# def search(request):
#     if request.method == "POST":
#         searched = request.POST['searched']
#         searched_product = Product.objects.filter(name__contains=searched)

#         return render (request,'search.html',{'searched':searched,'searched_product':searched_product}
#         )
#     else:
#         return render (request,'search.html',{}
#         )
def search_products(request):
    search_products = Product.objects.filter(name__icontains=request.POST.get('name'))
    products = Product.objects.all()
    context ={
        'products':products,
        'search_products':search_products
    }
    return render(request, 'search.html',context=context)