from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from django.db.models import Q
from .forms import *
from sslcommerz_lib import SSLCOMMERZ


def home(request):
    is_logged_in = False
    carts = None
    subtotal = 0
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
    product = Product.objects.order_by('-id')
    products = Product.objects.all()
    recents = BlogPost.objects.order_by('-id')

    context = {
        'is_user': is_logged_in,
        'product': product,
        'products': products,
        'blog': recents,
        'carts': carts,
        'subtotal': subtotal
    }
    return render(request, "home/index.html", context)


def myaccount(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.filter(user=request.user)
        orderItems = OrderItems.objects.filter(order__in=order)

        if profile.is_seller == 'on':
            return redirect('dashboard')
        else:
            context = {
                'is_user': is_logged_in,
                'profile': profile,
                'carts': carts,
                'subtotal': subtotal,
                'order': order,
                'orderitem': orderItems
            }
            return render(request, "home/myaccount.html", context)
    else:
        return redirect('SIGNIN')


def invoice(request, id):
    if request.user.is_authenticated:
        orderItems = OrderItems.objects.filter(order=id)
        profile = Profile.objects.get(user=request.user)
        order = Order.objects.get(id=id)
        context = {
            'orderitems': orderItems,
            'profile': profile,
            'orderid': id,
            'order': order
        }
        return render(request, "home/invoice.html", context)
    else:
        return redirect('SIGNIN')


def shop(request):
    is_logged_in = False
    carts = None
    subtotal = 0
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
    products = Product.objects.order_by("-id")
    pdImg = ProductImages.objects.all()
    obj = ProductCategory.objects.all()
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
        'carts': carts,
        'subtotal': subtotal
    }
    return render(request, "home/shop.html", context)


def detailsProduct(request, slug):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
    product = Product.objects.get(slug=slug)
    products = Product.objects.order_by("-id")
    pdImg = ProductImages.objects.filter(product=product)
    carts = []
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)

    if request.method == "POST":
        productid = request.POST.get('productId')
        quantitys = request.POST.get('quantity')
        quantity_ = int(quantitys)
        product_ = int(productid)
        try:
            cart = Cart.objects.get(Q(product=product_, user=request.user))
            cart.quantity += quantity_
            cart.save()
        except Cart.DoesNotExist:
            Cart(user=request.user, product=product, quantity=quantity_).save()
        return JsonResponse({'status': 'success'})

    context = {
        'is_user': is_logged_in,
        'product': product,
        'products': products,
        'pdImg': pdImg,
        'carts': carts,
        'subtotal': subtotal

    }
    return render(request, "home/detailsproduct.html", context)


def blog(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True

    blogs = BlogPost.objects.all()
    recents = BlogPost.objects.order_by('-id')
    carts = []
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)

    context = {
        'is_user': is_logged_in,
        "blogs": blogs,
        'recents': recents,
        'carts': carts,
        'subtotal': subtotal
    }
    return render(request, "home/blog.html", context)


def single_blog(request, slug):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True

    blog = BlogPost.objects.get(slug=slug)
    blogs = BlogPost.objects.order_by('-id')
    tag = blog.tag.split(",")
    carts = []
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)

    context = {
        'is_user': is_logged_in,
        'blog': blog,
        'blogs': blogs,
        'blog_tag': tag,
        'carts': carts,
        'subtotal': subtotal

    }
    return render(request, "home/single-blog.html", context)


def cart(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)

        if request.method == "POST":
            cartid = request.POST['cartId']
            quantity = request.POST['quantity']
            quantity = int(quantity)
            cart = Cart.objects.get(id=cartid)
            cart.quantity = quantity
            cart.save()
            carts_ = Cart.objects.filter(user=request.user)
            subtotal_ = get_subTotal(carts_)
            line_totals = []
            for i in carts_:
                line_totals.append(i.product.price * i.quantity)

            return JsonResponse({'status': 'success', 'subtotal': subtotal_, 'total': subtotal_, 'line_total': line_totals})

        context = {
            'is_user': is_logged_in,
            'carts': carts,
            'subtotal': subtotal
        }

        return render(request, "home/cart.html", context)
    else:
        return redirect('SIGNIN')


def add_to_cart(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        quantity_ = 1
        try:
            cart = Cart.objects.get(Q(product=product, user=request.user))
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            Cart(user=request.user, product=product, quantity=quantity_).save()
        return redirect('SHOP')
    else:
        return redirect('SIGNIN')


def deleteCart(request, id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(Q(user=request.user, id=id))
        cart.delete()
        return redirect('CART')


def checkoutPage(request):
    is_logged_in = False
    if request.user.is_authenticated:
        is_logged_in = True
        carts = Cart.objects.filter(user=request.user)
        if carts:
            subtotal = get_subTotal(carts)
            cfm = CustomerForm(request.POST)
            sfm = ShippingForm(request.POST)
            if request.method == "POST":
                if cfm.is_valid():
                    cfm.save()
                if sfm.is_valid():
                    sfm.save()

                payment_method = request.POST['payment_method']
                if payment_method == "online":
                    return redirect("payment")
                else:
                    customer_ = Customer.objects.order_by("-id")[:1].get()
                    shipping_ = Shipping.objects.order_by("-id")[:1].get()
                    order = Order(customer=customer_, shipping=shipping_,
                                  user=request.user, order_total=subtotal)
                    order.save()
                    order_ = Order.objects.order_by("-id")[:1].get()
                    for i in carts:
                        OrderItems(order=order_, product=i.product,
                                   quantity=i.quantity, user=request.user).save()
                    return redirect("myaccount")

            context = {
                'is_user': is_logged_in,
                'carts': carts,
                'subtotal': subtotal,
                'cform': cfm,
                'sform': sfm,
            }
            return render(request, "home/checkout.html", context)
        return redirect('SHOP')
    else:
        return redirect('SIGNIN')


# payment_method functionality
@csrf_exempt
def sslcommerz_success(request):
    print(request.user)
    # carts = Cart.objects.filter(user=request.user)
    # subtotal = get_subTotal(carts)
    # print(subtotal)
    # customer_ = Customer.objects.order_by("-id")[:1].get()
    # shipping_ = Shipping.objects.order_by("-id")[:1].get()
    # order = Order(customer=customer_, shipping=shipping_,
    #               user=request.user, order_total=subtotal)
    # order.save()
    # order_ = Order.objects.order_by("-id")[:1].get()
    # for i in carts:
    #     OrderItems(order=order_, product=i.product,
    #                quantity=i.quantity, user=request.user).save()
    return render(request, "home/success.html")


@csrf_exempt
def sslcommerz_failed(request):
    return render(request, "home/fail.html")


def sslcommerz_payment(request):
    carts = Cart.objects.filter(user=request.user)
    subtotal = get_subTotal(carts)
    user = request.user
    customer_ = Customer.objects.order_by("-id")[:1].get()
    shipping_ = Shipping.objects.order_by("-id")[:1].get()
    sslcz = SSLCOMMERZ({
        'store_id': 'shisa647c62f919419',
        'store_pass': 'shisa647c62f919419@ssl',
        'issandbox': True
    })

    data = {
        'total_amount': subtotal,
        'currency': "BDT",
        'tran_id': "tran_12345",
        'success_url': "http://127.0.0.1:8000/payment-success",
        'fail_url': "http://127.0.0.1:8000/payment-failed",
        'emi_option': "0",
        'cus_name': user,
        'cus_email': user.email,
        'cus_phone': customer_.phone,
        'cus_add1': customer_.Address,
        'cus_city': customer_.city,
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,
        'product_name': "Test",
        'product_category': "Test Category",
        'product_profile': "general",
    }
    response = sslcz.createSession(data)
    return redirect(response['GatewayPageURL'])


# custom function
def get_subTotal(carts):
    cartTotals = []
    for cart in carts:
        subtotal = cart.product.price*cart.quantity
        cartTotals.append(subtotal)
    return sum(cartTotals)

# it's not use right now


def carts(request):
    # if request.user.is_authenticated:
    try:
        carts = Cart.objects.filter(user=request.user)
        subtotal = get_subTotal(carts)
        return {'carts': carts, 'subtotal': subtotal}
    except Exception as e:
        pass
