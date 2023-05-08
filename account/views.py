from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from core.models import *
from .models import *
import random
from .sendcode import *


def signin(request):
    if not request.user.is_authenticated:
        msg = ""
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                profile = Profile.objects.get(user=user)
                if profile.is_seller == 'on':
                    login(request, user)
                    return redirect('dashboard')
                else:
                    login(request, user)
                    return redirect('myaccount')

            else:
                msg = "something wrong!! please try again."
        context = {
            'msg': msg
        }
        return render(request, "accounts/signin.html", context)
    else:
        return redirect('/dashboard')


def signout(request):
    logout(request)
    return redirect("HOME")


def signup(request):
    if not request.user.is_authenticated:
        msg = ""
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            avater = request.FILES.get('avater')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            seller = request.POST.get('seller')
            user_valid_check = User.objects.filter(username=username).exists()
            email_valid_check = User.objects.filter(email=email).exists()
            if user_valid_check or email_valid_check:
                msg = 'User name or Email already exist!!'
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
                profile = Profile.objects.create(user=user, avater=avater, phone=phone,address=address,is_seller=seller)
                user.is_active = False
                user.save()
                profile.save()
                otp = str(random.randint(100000, 999999))
                VerificationCode(code=otp, user=user).save()
                user_id = user.id
                sendOtp(first_name, otp, email)
                return redirect(f'otp/{user_id}')
        context = {
            'msg': msg
        }
        return render(request, 'accounts/registration.html', context)
    else:
        return redirect('/dashboard')


def otp(request, id):
    if not request.user.is_authenticated:
        user_id = id
        code = VerificationCode.objects.get(user_id=id)
        user = User.objects.get(id=user_id)
        otp = str(code)

        if request.method == "POST":
            code_ = request.POST.get('otp')
            if otp == code_:
                user.is_active = True
                user.save()
                code.delete()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed'})
        return render(request, 'accounts/otp.html', {'id': id})
    else:
        return redirect('/dashboard')


def success(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/success.html')
    else:
        return redirect('/dashboard')
