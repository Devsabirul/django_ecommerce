from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="HOME"),
    path('my-account', myaccount, name="myaccount"),
    path('invoice/<int:id>', invoice, name="invoice"),
    path('shop', shop, name="SHOP"),
    path('cart', cart, name="CART"),
    path('checkout', checkoutPage, name="checkoutPage"),
    path('add-to-cart/<int:id>', add_to_cart, name="ADD_TO_CART"),
    path('deleteCart/<int:id>', deleteCart, name="deleteCart"),
    path('product-details/<slug:slug>', detailsProduct, name="detailsProduct"),
    path('blog', blog, name="blog"),
    path('single_blog/<slug:slug>', single_blog, name="single_blog"),
    path('payment', sslcommerz_payment, name="payment"),
    path('payment-success', sslcommerz_success, name="sslcommerz_success"),
    path('payment-failed', sslcommerz_failed, name="sslcommerz_failed"),
]
