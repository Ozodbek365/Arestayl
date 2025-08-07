from itertools import product
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.template.defaulttags import comment
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class IndexView(View):
    def get(self, request):
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

        if request.user.is_authenticated:
            return render(request, 'index.html', context)
        return render(request, 'index-unauth.html', context)


class CategoryView(View):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        context = {
            'category': category
        }
        return render(request, 'category.html', context)


class SubCategoryView(LoginRequiredMixin,View):
    def get(self, request, category_slug, subcategory_slug):
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = Product.objects.filter(sub_category=subcategory).order_by('rating')

        countries = products.values_list('country', flat=True).distinct()
        brands = products.values_list('brand', flat=True).distinct()

        view = request.GET.get('view')
        filter_countries = request.GET.getlist('country')
        filter_brands = request.GET.getlist('brand')
        max_price = request.GET.get('max_price') if request.GET.get('max_price') !="" else None
        min_price = request.GET.get('min_price') if request.GET.get('min_price') !="" else None


        if filter_countries:
          products = products.filter(country__in=filter_countries)
        if filter_brands:
            products = products.filter(brand__in=filter_brands)
        if max_price is not None:
            products = products.filter(price__lte=max_price)
        if min_price is not None:
            products = products.filter(price__gte=min_price)

        paginator = Paginator(products, 2)

        pages = range(1, paginator.num_pages + 1)
        page = request.GET.get('page', 1)
        products = paginator.get_page(page)

        context = {
            'subcategory': subcategory,
            'view': view,
            'products': products,
            'countries': countries,
            'brands': brands,
            'filter_countries': filter_countries,
            'filter_brands': filter_brands,
            'max_price': max_price,
            'min_price': min_price,
            'pages': pages,
            'page': int(page),
            'pr_page': int(page) - 1 if int(page) > 1 else 1,
            'nt_page': int(page) + 1 if int(page) < paginator.num_pages else paginator.num_pages,
        }

        if view is not None:
            if view == 'large':
                return render(request, 'sub-products-large.html', context)
        return render(request, 'sub-products-grid.html', context)

class ProductView(View):

    def get(self, request, slug):
      product = get_object_or_404(Product, slug=slug)
      main_image_index = request.GET.get('mainImage')
      if main_image_index is None:
          main_image_index = 0
      main_image_index = int(main_image_index)

      main_image = product.image_set.all()[main_image_index]

      discounts = product.discount_set.all()
      if discounts.exists():
           discount = discounts.last()
           if discount.end_date > datetime.now():
               discount = None
      else:
          discount = None

          rating_percentage = product.rating / 5 * 100

      context = {
          'product': product,
          'mainImage': main_image,
          'discount': discount,
          'rating_percentage': rating_percentage,
      }
      print(rating_percentage)
      print(product.review_set.all().values_list('rating', flat=True))


      return render(request, 'product-info.html', context)

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        Review.objects.create(
            product=product,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment'),
            user=request.user
        )
        ratings = product.review_set.all().values_list('rating', flat=True)

        product.rating = sum(ratings) / len(ratings)
        product.save()

        return self.get(request, slug)


class WishListView(LoginRequiredMixin,View):
    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        context = {
            'favorites': favorites,
        }
        return render(request,'wishlist.html', context)


class AddToWishListView(LoginRequiredMixin,View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Favorite.objects.create(
            product=product, user=request.user
        )
        return redirect('wishlist')


class RemoveFromWishlist(LoginRequiredMixin, View):
    def get(self, request, favorite_id):
        favorite = get_object_or_404(Favorite, id=favorite_id)
        favorite.delete()
        return redirect('wishlist')



class AddToWishListForCartView(LoginRequiredMixin,View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        favorites = Favorite.objects.filter(user=request.user, product=product)
        if favorites.exists():
            favorites.delete()
            return redirect('my-cart')

        Favorite.objects.create(
            product=product, user=request.user
        )
        return redirect('my-cart')

