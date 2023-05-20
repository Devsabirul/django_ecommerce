from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.models import User
import os


def dashboard(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        products = Product.objects.filter(profile=profile).order_by('-id')
        blogs = BlogPost.objects.filter(profile=profile).order_by('-id')
        products = Product.objects.filter(profile=profile)
        order_item = OrderItems.objects.filter(product__in=products)
        total = 0
        # get total order
        for i in order_item:
            subtotal = i.product.price * i.quantity
            total = subtotal + total

        if profile.is_seller == 'on':
            context = {
                'profile': profile,
                'products': products,
                'blogs': blogs,
                'total': total
            }
            return render(request, 'index.html', context)
        else:
            return redirect('myaccount')
    else:
        return redirect('SIGNIN')


def blog_table(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        blogs = BlogPost.objects.filter(profile=profile).order_by('-id')

        context = {
            'profile': profile,
            'blogs': blogs
        }
        return render(request, 'blogs_table.html', context)
    else:
        return redirect('SIGNIN')


def product_table(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        products = Product.objects.filter(profile=profile).order_by('-id')
        context = {
            'profile': profile,
            'products': products
        }
        return render(request, 'products_table.html', context)
    else:
        return redirect('SIGNIN')


def order_table(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        products = Product.objects.filter(profile=profile)
        order_item = OrderItems.objects.filter(product__in=products)
        total = 0
        # get total order
        for i in order_item:
            subtotal = i.product.price * i.quantity
            total = subtotal + total

        context = {
            'profile': profile,
            'products': products,
            'order': order_item,
            'total': total
        }
        return render(request, 'order.html', context)
    else:
        return redirect('SIGNIN')


def tables(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        products = Product.objects.filter(profile=profile).order_by('-id')
        blogs = BlogPost.objects.filter(profile=profile).order_by('-id')
        context = {
            'profile': profile,
            'products': products,
            'blogs': blogs
        }
        return render(request, 'tables.html', context)
    else:
        return redirect('SIGNIN')


def add_product(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            pd_name = request.POST.get('pd_name')
            brand = request.POST.get('brand')
            productImages = request.FILES.getlist('productImages')
            category = request.POST.get('category').upper()
            description = request.POST.get('editor-1')
            availability = request.POST.get('availability')
            price = request.POST.get('price')
            # save category start
            ProductCategory(profile=profile, pd_category=category).save()
            # save product
            categoryobj = ProductCategory.objects.filter(
                profile=profile).order_by('-id')[:1].get()

            primaryimg = productImages[0]
            secondary = productImages[1]
            Product(pd_name=pd_name, brands=brand, description=description, price=price,
                    availability=availability, category=categoryobj, profile=profile, primary=primaryimg, secondary=secondary).save()

            # save product image
            product_ = Product.objects.filter(
                profile=profile).order_by('-id')[:1].get()

            for image in productImages:
                ProductImages.objects.create(
                    pd_iamges=image, product=product_, profile=profile).save()
        context = {
            'profile': profile
        }
        return render(request, 'add_product.html', context)
    else:
        return redirect('blog.slug')


def add_blog(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
            profile = Profile.objects.get(user=request.user)
            title = request.POST.get('title')
            description = request.POST.get('editor-1')
            tag = request.POST.get('tag')
            blogImages = request.FILES.get('blogImages')
            author = request.user.first_name
            blog = BlogPost(profile=profile, title=title, description=description,
                            tag=tag, blog_image=blogImages, author=author)
            blog.save()

        context = {
            'profile': profile
        }
        return render(request, 'add_blog.html', context)
    else:
        return redirect('account/signin')


def update_blog(request, id):
    if request.user.is_authenticated:
        blog = BlogPost.objects.get(id=id)
        profile = Profile.objects.get(user=request.user)
        if request.method == "POST":
            profile = Profile.objects.get(user=request.user)
            title = request.POST.get('title')
            description = request.POST.get('editor-1')
            tag = request.POST.get('tag')
            blogImages = request.FILES.get('blogImages')
            author = request.user.first_name
            if blogImages == None:
                blog = BlogPost(id=id, profile=profile, title=title, description=description,
                                tag=tag, blog_image=blog.blog_image, author=author)
                blog.save()
                return redirect("blog_table")
            else:
                blog_obj = BlogPost(id=id, profile=profile, title=title, description=description,
                                    tag=tag, blog_image=blogImages, author=author)
                os.remove(blog.blog_image.path)
                blog_obj.save()
                return redirect("blog_table")

        context = {
            'profile': profile,
            'blog': blog
        }
        return render(request, 'update_blog.html', context)
    else:
        return redirect('account/signin')


def update_product(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        profile = Profile.objects.get(user=request.user)
        image = ProductImages.objects.filter(product=product)
        if request.method == 'POST':
            pd_name = request.POST.get('pd_name')
            brand = request.POST.get('brand')
            category = request.POST.get('category').upper()
            description = request.POST.get('editor-1')
            availability = request.POST.get('availability')
            price = request.POST.get('price')
            # save category start
            ProductCategory(profile=profile, pd_category=category).save()
            # save product
            categoryobj = ProductCategory.objects.filter(
                profile=profile).order_by('-id')[:1].get()

            primaryimg = image[0].pd_iamges
            secondary = image[1].pd_iamges
            Product(id=id, pd_name=pd_name, brands=brand, description=description, price=price,
                    availability=availability, category=categoryobj, profile=profile, primary=primaryimg, secondary=secondary).save()
            return redirect("product_table")
        context = {
            'profile': profile,
            'product': product
        }
        return render(request, 'update_product.html', context)
    else:
        return redirect('account/signin')


def delete(request, id):
    blog = BlogPost.objects.get(id=id)
    os.remove(blog.blog_image.path)
    blog.delete()
    return redirect("blog_table")


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("product_table")
