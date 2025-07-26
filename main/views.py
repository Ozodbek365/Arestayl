from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            banner_index = 1
            categories = Category.objects.all()
            banners = Banner.objects.all()
            products = Product.objects.all()
            context = {
                'banners': banners,
                'banner_index': banner_index,
                'categories': categories,
                'products': products,
            }
            return render(request, 'index.html', context)
        return render(request, 'index-unauth.html')

class CategoryView(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        context = {
            'category': category
        }
        return render(request, 'category.html', context)


class SubCategoryView(LoginRequiredMixin,View):
    def get(self, request, subcategory_slug):
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        context = {
            'subcategory': subcategory
        }
        return render(request, 'sub-products-grid.html', context)