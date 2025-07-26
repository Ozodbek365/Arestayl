from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('<category_slug>/sub-categories/', CategoryView.as_view(), name='category'),
    path('<category_slug>/<subcategory_slug>/products/', SubCategoryView.as_view(), name='sub-category')
]