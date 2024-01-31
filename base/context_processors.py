from .models import Wishlist
from .models import Cart, ShippingOption
from django.db.models import Sum

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_count = wishlist.items.count()
    else:
        wishlist_count = 0
    return {'wishlist_count': wishlist_count}

def item_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
        items_in_cart = cart.items.all()
        total_cost = items_in_cart.aggregate(total=Sum('price'))['total'] or 0
    else:
        cart_count = 0
        items_in_cart = None
        total_cost = 0
    return {'cart_count': cart_count, 'items_in_cart':items_in_cart, 'total_cost':total_cost}
