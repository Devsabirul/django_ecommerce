from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField


class Profile(models.Model):
    avater = models.ImageField(
        upload_to="avater", null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    is_seller = models.CharField(max_length=15, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class ProductCategory(models.Model):
    pd_category = models.CharField(max_length=150, null=True, blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pd_category)


class Product(models.Model):
    pd_name = models.CharField(max_length=250)
    brands = models.CharField(max_length=150)
    description = RichTextField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    primary = models.ImageField(
        upload_to="Product Images", null=True, blank=True)
    secondary = models.ImageField(
        upload_to="Product Images", null=True, blank=True)
    availability = models.CharField(max_length=50, null=True, blank=True)
    slug = AutoSlugField(populate_from="pd_name", null=True, unique=True)
    price = models.PositiveIntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pd_name)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,null=True,blank=True)


    def line_total(self):
        return self.quantity * self.product.price

    

class ProductImages(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pd_iamges = models.ImageField(upload_to="Product Images")

    def __str__(self):
        return self.product.pd_name

class Customer(models.Model):
    country = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    Address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name
    

class Shipping(models.Model):
    shipping_country = models.CharField(max_length=100)
    shipping_first_name = models.CharField(max_length=100)
    shipping_last_name = models.CharField(max_length=100)
    shipping_company_name = models.CharField(max_length=100,null=True,blank=True)
    shipping_Address = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zipcode = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=100)

    def __str__(self):
        return self.shipping_first_name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField( auto_now=False, auto_now_add=True)
    status = models.CharField(max_length=100,default="panding")
    pymentSystem = models.CharField(max_length=100,default="cashondelivery")
    order_total = models.PositiveIntegerField(null=True,blank=True)
    ordernote = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.shipping.shipping_first_name

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

  

class BlogPost(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    blog_image = models.ImageField(upload_to="Blog Image")
    tag = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title
