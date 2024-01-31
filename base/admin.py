from django.contrib import admin
from .models import Category, Item, Wishlist, Cart, ShippingOption, Order, BillingDetails, PaymentMethod
# Register your models here.
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Wishlist)
admin.site.register(ShippingOption)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(BillingDetails)
admin.site.register(PaymentMethod)

