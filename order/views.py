from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from datetime import datetime
from .models import *


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = request.user.cartitem_set.all()
        wishlist_products = request.user.favorite_set.values_list('product__id', flat=True)

        # Discounts
        total_discount = 0
        total_price_without_discount = 0
        for cart_item in cart_items:
            total_price_without_discount += cart_item.product.price * cart_item.amount
            if cart_item.product.discount_set.filter(end_date__lt=datetime.today()).exists():
                discount = cart_item.product.discount_set.filter(
                    end_date__lt=datetime.today()).last().amount * cart_item.amount
                total_discount += discount

        total_price = total_price_without_discount - total_discount

        context = {
            'cart_items': cart_items,
            'wishlist_products': wishlist_products,
            'total_discount': total_discount,
            'total_price_without_discount': total_price_without_discount,
            'total_price': total_price,
        }
        return render(request, 'cart.html', context)

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart_items = CartItem.objects.filter(
            product=product,
            user=request.user
        )
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.amount += 1
            cart_item.save()
            return redirect('my-cart')

        CartItem.objects.create(
            product=get_object_or_404(Product, id=product_id),
            user=request.user
        )
        return redirect('my-cart')

class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        CartItem.objects.filter(
            product=get_object_or_404(Product, id=product_id),
            user=request.user
        ).delete()
        return redirect('my-cart')

def cart_item_inc(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.amount += 1
        cart_item.save()
        return redirect('my-cart')
    return redirect('login')

def cart_item_dec(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.amount == 1:
            cart_item.delete()
            return redirect('my-cart')
        cart_item.amount -= 1
        cart_item.save()
        return redirect('my-cart')
    return redirect('login')