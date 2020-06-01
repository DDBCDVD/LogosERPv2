from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.warehouse.models import stock_move
from apps.warehouse.models import stock_control
from apps.warehouse.models import products
from apps.warehouse.models import stock_location
from apps.warehouse.models import product_units
from apps.warehouse.models import products_package
from apps.warehouse.models import measurement_units


class products_model(admin.ModelAdmin):

    list_display = ("code", "name", "active", "description", "id")
    search_fields = ("code", "name", "active")
    list_filter = ("code", "name", "active")


class products_package_model(admin.ModelAdmin):

    list_display = ("code", "product_id", "pieces", "unit_qty", "location_id", "description", "id")
    search_fields = ("code", "product_id", "pieces", "unit_qty", "location_id")
    list_filter = ("code", "product_id", "pieces", "unit_qty", "location_id")


class product_units_model(admin.ModelAdmin):

    list_display = ("code", "name", "description", "quantity", "product_id", "id")
    search_fields = ("code", "name", "pieces", "quantity", "product_id")
    list_filter = ("code", "name", "pieces", "quantity", "product_id")


class stock_location_model(admin.ModelAdmin):
    list_display = ("code", "name", "location_type", "active", "description", "id")
    search_fields = ("code", "name", "location_type", "active")
    list_filter = ("code", "name", "location_type", "active")


class measurement_units_model(admin.ModelAdmin):
    list_display = ("code", "name", "unit_qty", "description", "id")
    search_fields = ("code", "name", "unit_qty")
    list_filter = ("code", "name", "unit_qty")


class stock_move_model(admin.ModelAdmin):

    list_display = ("code", "note", "package_id", "unit_id",
                    "pieces", "quantity", "location_id", "location_dest_id", "description", "id")
    search_fields = ("code", "package_id", "unit_id", "location_id", "location_dest_id", "quantity", "pieces")
    list_filter = ("code", "package_id", "unit_id", "location_id", "location_dest_id", "quantity", "pieces")


class stock_control_model(admin.ModelAdmin):

    list_display = ("code", "unit_id", "pieces", "quantity", "location_id", "id")
    search_fields = ("code", "unit_id", "pieces", "quantity", "location_id")
    list_filter = ("code", "unit_id", "pieces", "quantity", "location_id")


admin.site.register(products, products_model)
admin.site.register(products_package, products_package_model)
admin.site.register(product_units, product_units_model)
admin.site.register(stock_location, stock_location_model)
admin.site.register(measurement_units, measurement_units_model)
admin.site.register(stock_move, stock_move_model)
admin.site.register(stock_control, stock_control_model)