"""ERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from apps.warehouse import views as warehouse_views
from apps.warehouse.models import products
from apps.warehouse.models import stock_location
from apps.warehouse.models import product_units
from apps.warehouse.models import products_package
from apps.warehouse.models import measurement_units
from apps.warehouse.models import stock_move
from apps.warehouse.models import stock_control

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', warehouse_views.dashboard, name='dashboard'),
    path('test/', warehouse_views.test, name='test'),
    path('warehouse/', include('apps.warehouse.urls')),
]