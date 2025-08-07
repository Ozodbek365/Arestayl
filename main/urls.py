from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('<category_slug>/sub-categories/', CategoryView.as_view(), name='category'),
    path('<category_slug>/<subcategory_slug>/products/', SubCategoryView.as_view(), name='sub-category'),
    path('products/<slug:slug>/', ProductView.as_view(), name='product'),
    path('my-wishlist/', WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', AddToWishListView.as_view(), name='add-to-wishlist'),
    path('add-to-wishlist-for-cart/<int:product_id>/', AddToWishListForCartView.as_view(), name='add-to-wishlist-for-cart'),
    path('remove-from-wishlist/<int:favorite_id>/', RemoveFromWishlist.as_view(), name='remove-from-wishlist'),
]