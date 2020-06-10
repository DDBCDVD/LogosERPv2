from django.contrib import admin
from django.urls import path
from django.conf import settings
from apps.home import views as home_views
from apps.warehouse import views as warehouse_views
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit
from apps.warehouse.models import StockMove
from apps.warehouse.models import StockControl

urlpatterns = [

    path('dashboard/', home_views.dashboard, name='dashboard'),

]