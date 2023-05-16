from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(ProductCategory)


admin.site.register([Product,Cart])
admin.site.register(ProductImages)
admin.site.register(BlogPost)
admin.site.register([Customer,Shipping,Order])
admin.site.register(OrderItems)
