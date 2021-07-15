
""" Store URLs. """

# Django
from django.urls import  path

# View
from store import views

# Views
urlpatterns = [
 
    # Home page
    path(
        route='',
        view=views.store_view,
        name='store'
    ),
    # Cart
    path(
        route='cart/',
        view=views.cart_view,
        name='cart'
    ),
    # Checkout
    path(
        route='checkout/',
        view=views.checkout_view,
        name='checkout'
    ),

    # Update item
    path(
        route='update_item/',
        view=views.updateItem,
        name='update_item'
    ),

    # Process Order view
    path(
        route='process_order/',
        view=views.processOrder,
        name='process_order'
    ),

    # Process Order view
    path(
        route='nodeR/',
        view=views.nodeRed,
        name='nodeR'
    )


]

