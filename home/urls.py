from django.urls import path
from .views import home, products, productdetail, cart, add_to_cart, remove_from_cart, delete_from_cart, contact, about

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('products/', products, name='products'),
    path('productdetail/<int:id>/', productdetail, name='productdetail'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('delete-from-cart/', delete_from_cart, name='delete_from_cart'),
]