from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.db.models import Q


def home(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        product = Product.objects.order_by('-id')
        products = Product.objects.all()
        recents = BlogPost.objects.order_by('-id')
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)

        context = {
            'is_user': is_logged_in,
            'product': product,
            'products': products,
            'blog': recents,
            'carts':carts,
            'subtotal':subtotal
        }
        return render(request, "home/index.html", context)
    else:
        return redirect('SIGNIN')

def myaccount(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        profile = Profile.objects.get(user=request.user)
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
        if profile.is_seller == 'on':
            return redirect('dashboard')
        else:
            context = {
                'is_user': is_logged_in,
                'profile':profile,
                'carts':carts,
                'subtotal':subtotal
            }
            return render(request, "home/myaccount.html", context)
    else:
        return redirect('SIGNIN')
        


def shop(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
    products = Product.objects.order_by("-id")
    pdImg = ProductImages.objects.all()
    obj = ProductCategory.objects.all()
    carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)
    # get unique category start
    uCategory = dict()
    for unique in obj:
        if unique.pd_category in uCategory:
            uCategory[unique.pd_category] += 1
        else:
            uCategory[unique.pd_category] = 1
    # get unique category end

    context = {
        'is_user': is_logged_in,
        'products': products,
        'pdImg': pdImg,
        'categorie': uCategory,
        'carts':carts,
        'subtotal':subtotal
    }
    return render(request, "home/shop.html", context)


def detailsProduct(request, slug):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
    product = Product.objects.get(slug=slug)
    products = Product.objects.order_by("-id")
    pdImg = ProductImages.objects.filter(product=product)
    carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)

    if request.method == "POST":
        productid = request.POST.get('productId')
        quantitys = request.POST.get('quantity')
        quantity_ = int(quantitys)
        product_ = int(productid)
        try:
            cart = Cart.objects.get(Q(product=product_,user = request.user))
            cart.quantity += quantity_
            cart.save()
        except Cart.DoesNotExist:
            Cart(user=request.user,product=product,quantity=quantity_).save()
        return JsonResponse({'status': 'success'})

    context = {
        'is_user': is_logged_in,
        'product': product,
        'products': products,
        'pdImg': pdImg,
        'carts':carts,
        'subtotal':subtotal

    }
    return render(request, "home/detailsproduct.html", context)


def blog(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True

    blogs = BlogPost.objects.all()
    recents = BlogPost.objects.order_by('-id')
    carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)

    context = {
        'is_user': is_logged_in,
        "blogs": blogs,
        'recents': recents,
        'carts':carts,
        'subtotal':subtotal
    }
    return render(request, "home/blog.html", context)


def single_blog(request, slug):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True

    blog = BlogPost.objects.get(slug=slug)
    blogs = BlogPost.objects.order_by('-id')
    tag = blog.tag.split(",")
    carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)

    context = {
        'is_user': is_logged_in,
        'blog': blog,
        'blogs': blogs,
        'blog_tag': tag,
        'carts':carts,
        'subtotal':subtotal

    }
    return render(request, "home/single-blog.html", context)

def cart(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
        context = {
            'is_user': is_logged_in,
            'carts':carts,
            'subtotal':subtotal
        }

        return render(request, "home/cart.html", context)
    else:
        return redirect('SIGNIN')



def add_to_cart(request,id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        quantity_ = 1
        try:
            cart = Cart.objects.get(Q(product=product,user = request.user))
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            Cart(user=request.user,product=product,quantity=quantity_).save()
        return redirect('SHOP')
    else:
        return redirect('SIGNIN')

def deleteCart(request,id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(Q(user=request.user,id=id))
        cart.delete()
        return redirect('CART')


def checkoutPage(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        if carts:
            subtotal = get_subTotal(carts)
            context = {
                'is_user': is_logged_in,
                'carts':carts,
                'subtotal':subtotal
            }
            return render(request, "home/checkout.html", context)
        return redirect('SHOP')
    else:
        return redirect('SIGNIN')





# custom function 
def get_subTotal(carts):
    cartTotals = []
    for cart in carts:
        subtotal  = cart.product.price*cart.quantity
        cartTotals.append(subtotal)
    return sum(cartTotals)

# it's not use right now 
def carts(request):
    # if request.user.is_authenticated:
    try:
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
        return {'carts':carts,'subtotal':subtotal}
    except Exception as e:
        pass