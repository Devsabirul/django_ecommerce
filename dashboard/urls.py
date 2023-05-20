from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('add-product', add_product, name="add_product"),
    path('add-blog', add_blog, name="add_blog"),
    path('tables', tables, name="tables"),
    path('update-blog/<int:id>', update_blog, name="update_blog"),
    path('update-product/<int:id>', update_product, name="update_product"),
    path('delete-blog/<int:id>', delete, name="delete"),
    path('delete-product/<int:id>', deleteProduct, name="deleteProduct"),
    path('table-blog', blog_table, name="blog_table"),
    path('product-table', product_table, name="product_table"),
    path('order-table', order_table, name="order_table"),
]
