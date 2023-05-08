from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('add-product', add_product, name="add_product"),
    path('add-blog', add_blog, name="add_blog"),
    path('update-blog/<int:id>', update_blog, name="update_blog"),
    path('delete-blog/<int:id>', delete, name="delete"),
    path('table-blog', blog_table, name="blog_table"),
]
