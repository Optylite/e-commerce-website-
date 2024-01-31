from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
class ShippingOption(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    details  = models.TextField()

    def __str__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='GEMS/media/item-images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    auther = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return str(self.user)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return str(self.user)
    
class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    company = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    street_address2 = models.CharField(max_length=50, null=True)
    town_or_city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    order_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Item')
    shipping_option = models.ForeignKey(ShippingOption, on_delete=models.DO_NOTHING, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, null=True)
    is_delivered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)