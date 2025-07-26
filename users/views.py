from django.shortcuts import render, redirect, get_object_or_404
from django.views import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from random import randint

from unicodedata import category

from order.models import Order
from .models import *

from eskiz_sms import EskizSMS

email = "ozodbekalijonov365@gmail.com"
password = "a4kdoYclmzIia3adrrF9qp3lZ83iMOiDtbnHqgn8"

eskiz = EskizSMS(email, password)

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('password') == request.POST.get('repeat_password'):
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
            if user is not None:
                return self.get(request)
            user = User.objects.create_user(
                username=request.POST.get('phone'),
                phone=request.POST.get('phone'),
                password=request.POST.get('password'),
                gender=request.POST.get('gender'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                city=request.POST.get('city'),
                country=request.POST.get('country'),
            )
            confirmation_code = randint(100000, 999999)
            print(confirmation_code)
            user.confirmation_code = confirmation_code
            user.save()
            login(request, user)
            eskiz.send_sms(user.phone, 'Bu Eskiz dan test')
            return redirect('register-confirm')
        return self.get(request)

class RegisterConfirmView(View):
    def get(self, request):
        if request.user.is_authenticated:
           return render(request, 'register-confirm.html')
        return redirect('home')

    def post(self, request):
        if request.user.is_authenticated:
            confirmation_code = request.POST.get('confirmation_code')
            user = request.user
            if user.confirmation_code == confirmation_code:
                user.confirmed = True
                user.save()
                return redirect('home')
            return self.get(request)
        return redirect('home')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST.get('phone_number'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        return self.get(request)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProfileView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        awaiting_orders = user.order_set.exclude(status=Order.STATUS_CHOICES[3][0]).count()

        order_items = 0
        for order in user.order_set.all():
            order_items += order.orderitems_set.count()
        context = {
            'user': user,
            'awaiting_orders': awaiting_orders,
            'order_items': order_items,
        }
        return render(request, 'profile-main.html', context)


class ProfileSettings(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'profile-setting.html', context)

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.city = request.POST.get('city')
        user.country = request.POST.get('country')
        user.phone = request.POST.get('phone_number')
        user.username = request.POST.get('phone_number')
        user.save()
        return redirect('profile-settings')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProfileAddress(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'profile-address.html')


class ProfileOrders(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'profile-orders.html')


def logaut_view(request):
    logout(request)
    return redirect('home')

