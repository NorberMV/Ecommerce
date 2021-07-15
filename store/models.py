

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    


    # Fixed choice fields

    MOTOR_HP = (
         ('1.0', '1.0'),
         ('2.0', '2.0'),
         ('3.0', '3.0'),
         ('5.0', '5.0'),
         ('10.0', '10.0'),
    )

    MOTOR_SPEED = (
         ('1200', '1200'),
         ('1800', '1800'),
         ('3600', '3600'),
            
    )

    PHASES = (
        ('1', 'Single Phase'),
        ('3', 'Three Phase'),
    )

    PURPOSE = (
        ('General Purpose', 'General Purpose'),
        ('Pump', 'Pump'),
        ('Fan', 'Fan')
    )

     
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.CharField(max_length=600, null=True, blank=False) #widget=forms.Textarea
    
    # Fixed choice fields
    power = models.CharField(max_length=10, choices=MOTOR_HP, null=True, blank=True)
    speed = models.CharField(max_length=10, choices=MOTOR_SPEED, null=True)
    phases_number = models.CharField(max_length=10, choices=PHASES, null=True)
    purpose = models.CharField(max_length=15, choices=PURPOSE, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name # This variable is going to be visible when I make a query
    
    # This decorator avoid the error when an image file is empty
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)

    # Set the logic to shipping or not shipping address
    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()

        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    
    # To sum the total cost of each of the order items
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([ orderitem.get_total for orderitem in orderitems])
        return total
    
    # To sum each of the order items quantity
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([orderitem.quantity for orderitem in orderitems])
        return total
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) 
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.name)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True) # Check this
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


