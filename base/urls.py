from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('details/<pk>/', views.details, name='details'),
    path('section/<pk>/', views.section, name='section'),
    path('popup/<pk>/', views.popup, name='popup'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
     path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('new_product/', views.new, name='new_product'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('checkout/', views.checkout, name='checkout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/password_change/done/'), name='password_change'),
    path('order/<int:order_id>/', views.orderitem, name='order_item'),
    path('edit_details', views.edit_details, name='edit_details'),
    path('edit_shipping_address', views.edit_shipping_address, name='edit_shipping_address'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
