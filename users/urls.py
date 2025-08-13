from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logaut_view, name='logaut'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register-confirm/', RegisterConfirmView.as_view(), name='register-confirm'),
]

urlpatterns += [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', ProfileSettings.as_view(), name='profile-settings'),
    path('profile/address/', ProfileAddress.as_view(), name='profile-address'),
]