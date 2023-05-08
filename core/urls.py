from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="HOME"),
    path('my-account', myaccount, name="myaccount"),
    path('shop', shop, name="SHOP"),
    path('cart', cart, name="CART"),
    path('checkout', checkoutPage, name="checkoutPage"),
    path('add-to-cart/<int:id>', add_to_cart, name="ADD_TO_CART"),
    path('deleteCart/<int:id>', deleteCart, name="deleteCart"),
    path('product-details/<slug:slug>', detailsProduct, name="detailsProduct"),
    path('blog', blog, name="blog"),
    path('single_blog/<slug:slug>', single_blog, name="single_blog"),
]
