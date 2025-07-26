from django.contrib import admin
from .models import *

admin.site.register(
    [
        Category, SubCategory, Product, Image, Review, Favorite, Discount, Banner
    ]
)
