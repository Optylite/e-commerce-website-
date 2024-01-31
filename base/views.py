
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.contrib.auth import update_session_auth_hash
from .models import Category, Item, Wishlist, Cart, ShippingOption, Order, PaymentMethod, BillingDetails
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUp, NewItemForm, DetailsForm, OrderForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserChangeForm
# Create your views here.
def home(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    context = {'items':items, 'categories':categories}
    return render(request, 'base/home.html', context)

def contact(request):
    return render(request, 'base/contact.html')

def shop(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    items = Item.objects.filter(Q(category__name__icontains=q)|
                                Q(name__icontains=q)|
                                Q(price__icontains=q)).order_by('-created')
    categories = Category.objects.all()
    context = {'items':items, 'categories':categories}
    return render(request, 'base/shop.html', context)

def signup_page(request):
    form = SignUp()
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('an error occurred')

    context = {'form':form}
    return render(request, 'base/signup.html', context)

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
       return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('user does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('username or password is wrong')
    context = {'page':page}
    return render(request, 'base/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def section(request, pk):
    category = Category.objects.get(pk=pk)
    items = Item.objects.filter(is_sold=False, category=category)
    categories = Category.objects.all()
    context = {'category':category, 'items':items, 'categories':categories}
    return render (request, 'base/section.html', context)

def details(request, pk):
    items = get_object_or_404(Item, pk=pk)
    categories = Category.objects.all()
    related = Item.objects.filter(category=items.category, is_sold=False).exclude(pk=pk)[0:3]
    context = {'items':items, 'related':related, 'categories':categories}
    return render (request, 'base/details.html', context)

def popup(request, pk):
    items = get_object_or_404(Item, pk=pk)
    context = {'items':items}
    return render (request, 'base/popup.html', context)

@login_required(login_url='/login/')
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    # Store the previous page's URL in the session
    request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.items.add(item)

    # Redirect to the previous page
    return redirect(request.session['previous_page'])

@login_required(login_url='/login/')
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items_in_wishlist = wishlist.items.all()
    wishlist_count = items_in_wishlist.count()
    context = {'wishlist_count':wishlist_count,'wishlist': items_in_wishlist}
    return render(request, 'base/wishlist.html', context)

@login_required(login_url='/login/')
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.items.remove(item)
    return redirect('wishlist')

@login_required(login_url='/login/')
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)

    request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.add(item)
    return redirect(request.session['previous_page'])

@login_required(login_url='/login/')
def cart(request):
    # Retrieve the first cart or create a new one
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)

    items_in_cart = cart.items.all()
    cart_count = items_in_cart.count()
    shipping_option = ShippingOption.objects.all()
    payment_method = PaymentMethod.objects.all()

    # Calculate total cost of items in the cart
    total_cost = items_in_cart.aggregate(total=Sum('price'))['total'] or 0

    if request.method == 'POST':
        selected_shipping_id = request.POST.get('shipping')
        selected_payment_method_id = request.POST.get('payment')

        if selected_shipping_id:
            try:
                shipping_option = ShippingOption.objects.get(pk=selected_shipping_id)
                payment_method = PaymentMethod.objects.get(pk=selected_payment_method_id)

                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    total_cost=total_cost + shipping_option.cost,
                    shipping_option=shipping_option,
                    payment_method=payment_method,
                )

                # Associate the items with the order
                order.items.add(*cart.items.all())

                # Clear the items from the cart
                cart.items.clear()


                return redirect('checkout')
            except ShippingOption.DoesNotExist:
                return HttpResponse('Selected shipping option does not exist.')
        return redirect('checkout')

    context = {'cart_count': cart_count, 'cart': items_in_cart, 'total_cost': total_cost, 'shipping_option': shipping_option, 'payment_method': payment_method}
    return render(request, 'base/cart.html', context)


@login_required(login_url='/login/')
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid:
            item = form.save(commit=False)
            item.auther = request.user
            item.save()
            return redirect('details', pk=item.id)
        
    else:
        form = NewItemForm()
    
    context = {'form':form}
    return render(request, 'base/new_product.html', context)

@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('shop')  # Redirect to a success page
    else:
        form = DetailsForm()
    context = {'form':form}
    return render(request, 'base/checkout.html', context)

@login_required(login_url='/login/')
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user = request.user
            cart_items = Cart.objects.filter(user=user).values_list('items', flat=True)
            shipping_option = form.cleaned_data['shipping_option']

            # Calculate total cost based on items in the cart and selected shipping option
            total_cost = calculate_total_cost(cart_items, shipping_option)

            # Create the order
            order = Order.objects.create(
                user=user,
                shipping_option=shipping_option,
                total_cost=total_cost
            )

            # Add items to the order
            order.items.set(cart_items, cart_items.id)

            # Optionally, clear the user's cart after creating the order
            Cart.objects.get(user=user).items.clear()

            return redirect('order_success')  # Redirect to a success page
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})

def calculate_total_cost(request, cart_items):
    # Implement your logic to calculate the total cost
    # You may need to query the prices of the items and the cost of the selected shipping option
    # and perform any necessary calculations
    z = cart_items.aggregate(total=Sum('price'))['total'] or 0
    
    total_cost = z
    return (request, 'base/checkout.html', {'total_cost':total_cost})

@login_required(login_url='/login/')
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.remove(item)
    return redirect('cart')


@login_required(login_url='/login/')
def dashboard(request):
    host = request.user
    all_orders = Order.objects.filter(user=request.user)
    billing_details= BillingDetails.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for maintaining the user's session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)


    context={'all_orders':all_orders, 'host':host, 'billing_details':billing_details, 'form': form }
    return render(request, 'base/dashboard.html', context)

def edit_billing_details(request):
    user_billing_details = BillingDetails.objects.get(user=request.user)

    if request.method == 'POST':
        form = DetailsForm(request.POST, instance=user_billing_details)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page or any other desired page after editing
    else:
        form = DetailsForm(instance=user_billing_details)

    return render(request, 'edit_billing_details.html', {'form': form})

def orderitem(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'base/order_item.html', {'order': order})

@login_required
def edit_details(request):
    user = request.user
    billing_details, created = BillingDetails.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username', '')
        user.save()

        billing_details.firstname = request.POST.get('firstname', '')
        billing_details.lastname = request.POST.get('lastname', '')
        billing_details.company = request.POST.get('company', '')
        billing_details.phone_number = request.POST.get('phone_number', '')
        billing_details.email = request.POST.get('email', '')
        billing_details.save()

        return redirect('dashboard')  # Redirect to user's profile page after saving changes

    return render(request, 'base/edit_details.html', {'billing_details': billing_details, 'user': user})

@login_required
def edit_shipping_address(request):
    user = request.user
    billing_details, created = BillingDetails.objects.get_or_create(user=user)

    if request.method == 'POST':
        billing_details.town_or_city = request.POST.get('town_or_city', '')
        billing_details.street_address = request.POST.get('street_address', '')
        billing_details.state = request.POST.get('state', '')
        billing_details.postal_code = request.POST.get('postal_code', '')
        billing_details.country = request.POST.get('country', '')
        billing_details.save()

        return redirect('dashboard')  # Redirect to user's profile page after saving changes

    return render(request, 'base/edit_shipping_address.html', {'billing_details': billing_details, 'user': user})
