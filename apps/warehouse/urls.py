from django.contrib import admin
from django.urls import path
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
    
    #-------------------------------------------PRODUCTS MODEL--------------------------------------#
    path('ListProduct/', 
        warehouse_views.ListProduct.as_view(
            model=products, extra_context={'heading': 'Productos', 'title': 'Productos'}), name='ListProduct'),    
    path('DetailProduct/<int:pk>/', 
        warehouse_views.DetailProduct.as_view(
            model=products, extra_context={'title': 'Detalle Producto'}), name='DetailProduct'),
    path('CreateProduct/', 
        warehouse_views.CreateProduct.as_view(
            extra_context={'heading': 'Creando Producto', 'title': 'Crear Producto'}, model=products), name='CreateProduct'),
    path('EditProduct/<int:pk>/', warehouse_views.EditProduct.as_view(
        extra_context={'heading': 'Editando Producto', 'title': 'Editar Producto'}, model=products), name='EditProduct'),
    path('DeleteProduct/<int:pk>/', warehouse_views.DeleteProduct.as_view(
        model=products, extra_context={'heading': 'Eliminar Producto', 'title': 'Eliminar Producto'}), name='DeleteProduct'),

    #-------------------------------------------PRODUCT UNIT MODEL--------------------------------------#
    path('ListProductUnit/', warehouse_views.ListProductUnit.as_view(
        extra_context={'heading': 'Unidades de Producto', 'title': 'Unidades de Producto'}, model=product_units), name='ListProductUnit'),
    path('DetailProductUnit/<int:pk>/', warehouse_views.DetailProductUnit.as_view(
        extra_context={'title': 'Detalles'}, model=product_units), name='DetailProductUnit'),    
    path('CreateProductUnit/', warehouse_views.CreateProductUnit.as_view(
        extra_context={'heading': 'Creando Unidad', 'title': 'Crear Unidad'}, model=product_units), name='CreateProductUnit'),
    path('EditProductUnit/<int:pk>/', warehouse_views.EditProductUnit.as_view(
        extra_context={'heading': 'Editando Unidad', 'title': 'Editar Unidad'}, model=product_units), name='EditProductUnit'),
    path('DeleteProductUnit/<int:pk>/', warehouse_views.DeleteProductUnit.as_view(model=product_units), name='DeleteProductUnit'),

    #------------------------------------------STOCK LOCATION MODEL--------------------------------#
    path('ListStockLocation/', warehouse_views.ListStockLocation.as_view(
        extra_context={'heading': 'Ubicaciones', 'title': 'Ubicaciones'}, model=stock_location), name='ListStockLocation'),
    path('CreateStockLocation/', warehouse_views.CreateStockLocation.as_view(
        extra_context={'heading': 'Creado Ubicación', 'title': 'Crear Ubicación'}, model=stock_location), name='CreateStockLocation'),
    path('EditStockLocation/<int:pk>/', warehouse_views.EditStockLocation.as_view(
        extra_context={'heading': 'Editando Ubicación', 'title': 'Editar Ubicación'}, model=stock_location), name='EditStockLocation'),
    path('DeleteStockLocation/<int:pk>/', warehouse_views.DeleteStockLocation.as_view(model=stock_location), name='DeleteStockLocation'),
    path('DetailStockLocation/<int:pk>/', warehouse_views.DetailStockLocation.as_view(
        extra_context={'title': 'Detalles'}, model=stock_location), name='DetailStockLocation'),  

    #--------------------------------------PRODUCTS PACKAGE MODEL-----------------------------------------#
    path('ListProductPackage/', warehouse_views.ListProductPackage.as_view(
        extra_context={'heading': 'Paquetes', 'title': 'Paquetes de Productos'}, model=products_package), name='ListProductPackage'),    
    path('DetailProductPackage/<pk>/', warehouse_views.DetailProductPackage.as_view(
        extra_context={'heading': 'Detalle del Paquete', 'title': 'Detalle del Paquete'}, model=products_package), name='DetailProductPackage'),
    path('CreateProductPackage/', warehouse_views.CreateProductPackage.as_view(
        extra_context={'heading': 'Creando Paquetes', 'title': 'Crear Paquete'}, model=products_package), name='CreateProductPackage'),
    path('EditProductPackage/<int:pk>/', warehouse_views.EditProductPackage.as_view(
        extra_context={'heading': 'Editando Paquete', 'title': 'Editar Paquete'}, model=products_package), name='EditProductPackage'),
    path('DeleteProductPackage/<int:pk>/', warehouse_views.DeleteProductPackage.as_view(model=products_package), name='DeleteProductPackage'),
    path('create_unit_package/<int:pk>/', warehouse_views.create_unit_package, name='create_unit_package'),

    #--------------------------------------MEASUREMENT UNITS MODEL-----------------------------------------#
    path('ListMeasurementUnit/', warehouse_views.ListMeasurementUnit.as_view(
        extra_context={'heading': 'Unidades de Medida', 'title': 'Unidades de Medida'}, model=measurement_units), name='ListMeasurementUnit'),
    path('CreateMeasurementUnit/', warehouse_views.CreateMeasurementUnit.as_view(
        extra_context={'heading': 'Creando Unidad de Medida', 'title': 'Crear Unidad de Medida'}, model=measurement_units), name='CreateMeasurementUnit'),
    path('EditMeasurementUnit/<int:pk>/', warehouse_views.EditMeasurementUnit.as_view(
        extra_context={'heading': 'Editando Unidad de Medida', 'title': 'Editar Unidad de Medida'}, model=measurement_units), name='EditMeasurementUnit'),
    path('DeleteMeasurementUnit/<int:pk>/', warehouse_views.DeleteMeasurementUnit.as_view(model=measurement_units), name='DeleteMeasurementUnit'),

    #--------------------------------------STOCK MOVE MODEL-----------------------------------------#
    path('ListStockMove/', warehouse_views.ListStockMove.as_view(
        extra_context={'heading': 'Movimientos de Stock', 'title': 'Movimientos de Stock'}, model=stock_move), name='ListStockMove'),    
    path('DetailStockMove/<pk>', warehouse_views.DetailStockMove.as_view(
        extra_context={'title': 'Detalle'}, model=stock_move), name='DetailStockMove'),
    path('function_create_move_package/', warehouse_views.function_create_move_package, name='function_create_move_package'),
    path('function_create_move_unit/', warehouse_views.function_create_move_unit, name='function_create_move_unit'),
    #--------------------------------------STOCK CONTROL MODEL-----------------------------------------#
    path('ListStockControl/', warehouse_views.ListStockControl.as_view(
        extra_context={'heading': 'Controles de Stock', 'title': 'Control de Stock'}, model=stock_control), name='ListStockControl'),
]