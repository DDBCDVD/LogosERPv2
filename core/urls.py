from django.contrib import admin
from django.urls import path
from django.conf import settings
from core import views as core_views
from apps.warehouse.models import Product

urlpatterns = [

    #  -----------------------------HOME--------------------#
    path('dashboard/', core_views.dashboard.as_view(), name='dashboard'),

    #  -----------------------------LOGIN--------------------#
    path('login/', core_views.Login.as_view(
        extra_context={'title': 'Login'}), name='login'),

    path('logout/', core_views.LogoutView.as_view(
        extra_context={'title': 'Logout'}), name='logout')
]