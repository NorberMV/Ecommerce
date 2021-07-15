

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import datetime
# Models
from .models import * # Import all models from this folder

# Forms
from store.forms import MotorFilterForm

# Utilities
import pdb
from . utils import cookieCart, cartData, guestOrder

# Create your views here.


def store_view(request):
    """ The main store view."""
    # AUTHENTICATED VALIDATION CODE
    # For authenticated users
    if request.user.is_authenticated:
        customer = request.user.customer
        # Creates a empty order with the field "complete" set to False
        order, created = Order.objects.get_or_create(customer=customer, 
            complete=False
        ) # Search for an order that has already incomplete or create a new
        items = order.orderitem_set.all() # Querying the child objects within orderitems
        cartItems = order.get_cart_items
        #pdb.set_trace()
    # For unauthenticated users
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    # FILTER CODE    
    # return HttpResponse('Ecommerce App!')
    products = Product.objects.all() # Making the Query
    #pdb.set_trace()
    
    if request.method =='POST':
        """ If the formulary has been submitted [ the filter button has been pressed, then the following queryset is sent: (Pdb) request.POST <QueryDict: {'csrfmiddlewaretoken': ['oNfJlX2vP6bF32DSk6LGpA6A8HUoqgp4l3K02yUORlk5Mzm66vhL2tATsdJMFhoX'], 'power': ['1.0']}>]"""
        form = MotorFilterForm(request.POST) # Load the form, create a form instance and populate it with data from the request
        #pdb.set_trace()
        # check whether it's valid:
        if form.is_valid():
            
            # Filtering
            hp_query = request.POST.get('power') 
            speed_query = request.POST.get('speed') 
            phases_query = request.POST.get('phases')
            purpose_query = request.POST.get('purpose')

            #pdb.set_trace()
            
            if hp_query != ' ' and hp_query is not None:
                products = products.filter(power=hp_query)

            if speed_query != ' ' and speed_query is not None:
                products = products.filter(speed=speed_query)

            if phases_query != ' ' and phases_query is not None:
                products = products.filter(phases_number=phases_query)

            if purpose_query != ' ' and purpose_query is not None:
                products = products.filter(purpose=purpose_query)

    else: # if a GET (or any other method) we'll create a blank form
        form = MotorFilterForm() # Send an empty formulary
        #products = Product.objects.all() # Making the Query
        #order = {'get_cart_total':0, 'get_cart_items':0} # Send this empty dict to avoid error on the browser
        #cartItems = order['get_cart_order']

    return render(
        request=request,
        template_name='store/store.html',
        context={
            'products': products, # Envía el contexto al template
            'form': form,
            'cartItems': cartItems,
        }
    )

def cart_view(request):
    
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

        #pdb.set_trace()

    return render(
        request=request,
        template_name='store/cart.html',
        context={
            'items': items,
            'order': order,
            'cartItems': cartItems,
            
        }
    )

def checkout_view(request):

    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']


    return render(
        request=request,
        template_name='store/checkout.html',
        context={
            'items': items,
            'order': order,
            'cartItems': cartItems,
        }
    )

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    #pdb.set_trace()

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1 )
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1 )
    
    orderItem.save()
    
    if orderItem.quantity  <= 0:
        orderItem.delete()

    print('Action:', action)
    print('productId:', productId)

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body) # Receive the form & shipping info data from "checkout.html" javascript
    #pdb.set_trace()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer, order = guestOrder(request, data)
        


    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total): # If the frontend total value is equal to the backend total value
        order.complete = True
    order.save()
            #pdb.set_trace()
    if order.shipping == True:

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )


    return JsonResponse('Payment complete!', safe=False) # Send response data to javascript







def nodeRed(request):

    if request.method == 'POST':
        data = request.POST
    else:
        data ={}

    return render(
        request=request,
        template_name='store/nodeR.html',
        context={
            'data': data,
        }
    )