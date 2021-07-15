
import json
from . models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart']) # cart: {'2': {'quantity': 1}, '3': {'quantity': 1}}
    except:
        cart = {}

    print('cart: {}'.format(cart))
    # pdb.set_trace()
    #order = dict()
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False} # Becouse I can´t modify the DB, Send this empty dict to avoid error on the browser
    items = list()

    for key, value in cart.items(): # Iterares on the dictionary cart pairs "key":"value" => cart: {'2': {'quantity': 1}, '3': {'quantity': 1}}
        
        try:
            order['get_cart_items'] += value['quantity'] # Acummulates the quantity value and saves it on the cartItems to render on the cart Icon
            product = Product.objects.get(id=key) # A full object of the product selected   
            order['get_cart_total'] += product.price * value['quantity']
            
            item = {

                'product':{
                    'id': key,
                    'name': product.name, 
                    'price':product.price,
                    'imageURL':product.imageURL,
                    }, 
                'quantity':value['quantity'],
                'get_total': product.price * value['quantity'],
            }
            items.append(item)
            

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
            
        #pdb.set_trace()
    cartItems = order['get_cart_items']

    return {
        'items':items,
        'order':order,
        'cartItems':cartItems,        
    }


def cartData(request):  
    # For authenticated users
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, 
            complete=False
        )# Search for an order that has already incomplete or create a new
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        # pdb.set_trace()
    
    # For unauthenticated users
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return {
        'items': items,
        'order': order,
        'cartItems':cartItems,

    }

def guestOrder(request, data):
    print('The user isn´t logged in.')
    print('Cookies: ', request.COOKIES)
    #pdb.set_trace()

    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # Creating the customer
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    # Creating the order
    order = Order.objects.create( 
        customer=customer,
        complete=False,
        )
    
    for item in items:  # Iterates into the items list
        
        product = Product.objects.get(id=item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product= product,
            order = order,
            quantity = item['quantity'],
        )
    return customer, order
