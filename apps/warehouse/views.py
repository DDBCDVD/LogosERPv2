from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import DeleteView, DetailView
#  from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
import apps.warehouse.validations as validations
import apps.warehouse.functions as functions
from apps.warehouse.models import products
from apps.warehouse.models import stock_location
from apps.warehouse.models import product_units
from apps.warehouse.models import products_package
from apps.warehouse.models import measurement_units
from apps.warehouse.models import stock_move
from apps.warehouse.models import stock_control
from apps.warehouse.forms import ProductForm
from apps.warehouse.forms import StockLocationForm
from apps.warehouse.forms import ProductUnitForm
from apps.warehouse.forms import ProductPackageForm
from apps.warehouse.forms import MeasurementUnitForm
from apps.warehouse.forms import MovePackageForm
from apps.warehouse.forms import MoveUnitForm


def dashboard(request):
    return render(request, "dashboard.html")


# def test(request):
#     data = {
#         'nombre': 'daniel'
#     }

#     return JsonResponse(data)

def test(request):
    return render(request, "tests/test_modal.html")

# -------------------------------PRODUCTS MODEL-----------------------#

# ------------------------VIEWS------------------------------#


# @method_decorator(login_required, name='dispatch')
class ListProduct(ListView):

    model = products
    create_form = ProductForm
    template_name = 'products/views/ListProduct.html'
    success_url = reverse_lazy('ListProduct')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nuevo Producto'
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProduct(DetailView):
    model = product_units
    stock_move = stock_move
    template_name = 'products/views/DetailProduct.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        unit_ids = product_units.objects.filter(product_id=product_id)
        package_ids = products_package.objects.filter(product_id=product_id)
        heading = 'Detalle %s' % product_id.code
        context['heading'] = heading
        context['unit_lines'] = 'Unidades Asociadas'
        context['pckg_lines'] = 'Paquetes Asociados'
        if unit_ids:
            context['unit_ids'] = unit_ids
        if package_ids:
            context['package_ids'] = package_ids
        return context
# ------------------------FUNCTIONS------------------------------#


class CreateProduct(CreateView):
    model = products
    addform = MeasurementUnitForm
    form_class = ProductForm
    template_name = 'products/functions/CreateProduct.html'
    success_url = reverse_lazy('ListProduct')
    creating = reverse_lazy('CreateProduct')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headitem'] = 'Add Measure'
        context['addform'] = self.addform()
        context['model_data'] = self.model.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        addform_data = self.addform(request.POST)
        new_item = self.form_class(request.POST)
        if addform_data.is_valid():
            addform_data.save()
            return HttpResponseRedirect(self.creating)
        elif new_item.is_valid():
            new_item.save()
            return HttpResponseRedirect(self.success_url)


class EditProduct(UpdateView):
    model = products
    form_class = ProductForm
    template_name = 'products/functions/CreateProduct.html'
    success_url = reverse_lazy('ListProduct')


class DeleteProduct(DeleteView):
    model = products
    form_class = ProductForm
    template_name = 'products/functions/DeleteProduct.html'
    success_url = reverse_lazy('ListProduct')


# --------------------PRODUCT UNIT MODEL----------------------------#

# ------------------------VIEWS------------------------------#


class ListProductUnit(ListView):

    model = product_units
    create_form = ProductUnitForm
    template_name = 'product_units/views/ListProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nueva Unidad de Producto'
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProductUnit(DetailView):
    model = product_units
    template_name = 'product_units/views/DetailProductUnit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        move_ids = stock_move.objects.filter(unit_id=unit_id)
        heading = 'Detalle %s' % unit_id.code
        context['heading'] = heading
        context['move_heading'] = 'Movimientos'
        context['item_type'] = 'Unit'
        if move_ids:
            context['move_ids'] = move_ids
        if unit_id.package_id:
            print(unit_id.package_id.code)
            move_pckg_ids = stock_move.objects.filter(
                package_id=unit_id.package_id.id)
            if move_pckg_ids:
                context['move_pckg_ids'] = move_pckg_ids
                context['pckg_moves'] = 'Movimientos del Paquete'
        else:
            print('No hay paquete asociado')
        return context


# ------------------------FUNCTIONS------------------------------#

class CreateProductUnit(CreateView):
    model = product_units
    addform = ProductForm
    form_class = ProductUnitForm
    template_name = 'product_units/functions/CreateProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')


class EditProductUnit(UpdateView):
    model = product_units
    form_class = ProductUnitForm
    template_name = 'product_units/functions/CreateProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')


class DeleteProductUnit(DeleteView):
    model = product_units
    form_class = ProductUnitForm
    template_name = 'product_units/functions/DeleteProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')


# --------------------STOCK LOCATION MODEL--------------------------#

# ------------------------VIEWS------------------------------#
class ListStockLocation(ListView):
    model = stock_location
    # paginate_by = 20
    template_name = 'stock_location/views/ListStockLocation.html'


class DetailStockLocation(DetailView):
    model = stock_location
    template_name = 'stock_location/views/DetailStockLocation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        stkctrl_ids = stock_control.objects.filter(location_id=location_id)
        pckg_ids = products_package.objects.filter(location_id=location_id)
        heading = 'Detalle %s' % location_id.code
        context['heading'] = heading
        context['controls_lines'] = 'Stock en esta ubicación'
        context['pckg_lines'] = 'Paquetes en esta ubicación'
        if stkctrl_ids:
            context['stkctrl_ids'] = stkctrl_ids
        if pckg_ids:
            context['pckg_ids'] = pckg_ids
        return context
# ------------------------FUNCTIONS------------------------------#


class CreateStockLocation(CreateView):
    model = stock_location
    form_class = StockLocationForm
    template_name = 'stock_location/functions/CreateStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')


class EditStockLocation(UpdateView):
    model = stock_location
    form_class = StockLocationForm
    template_name = 'stock_location/functions/CreateStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')


class DeleteStockLocation(DeleteView):
    model = stock_location
    form_class = StockLocationForm
    template_name = 'stock_location/functions/DeleteStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')


# -----------------------PRODUCT PACKAGE MODEL-----------------------#

# ------------------------VIEWS------------------------------#
class ListProductPackage(ListView):

    model = products_package


    model = products_package
    template_name = 'products_package/views/ListProductPackage.html'
    create_form = ProductPackageForm
    success_url = reverse_lazy('ListProductPackage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nuevo Paquete'
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProductPackage(DetailView):
    model = products_package
    template_name = 'products_package/views/DetailProductPackage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        move_ids = stock_move.objects.filter(package_id=package_id.id)
        unit_ids = product_units.objects.filter(package_id=package_id.id)

        heading = 'Detalle %s' % package_id.code
        context['heading'] = heading
        context['move_heading'] = 'Movimientos'
        context['lines_heading'] = 'Unidades del Paquete'
        context['item_type'] = 'Package'
        if move_ids:
            context['move_ids'] = move_ids
            context['unit_ids'] = unit_ids
        return context


# ------------------------FUNCTIONS------------------------------#

class CreateProductPackage(CreateView):
    model = products_package
    form_class = ProductPackageForm
    template_name = 'products_package/functions/CreateProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')


class EditProductPackage(UpdateView):
    model = products_package
    form_class = ProductPackageForm
    template_name = 'products_package/functions/CreateProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')


class DeleteProductPackage(DeleteView):
    model = products_package
    form_class = ProductPackageForm
    template_name = 'products_package/functions/DeleteProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')


def create_unit_package(request, pk):
    '''
    Create multiple product_unit from this package

    '''
    package = products_package.objects.filter(id=pk)
    for pckg in package:
        if pckg.units_created:
            messages.info(
                request, 'The units of this package were already created')
        else:
            if pckg.unit_qty:
                # Pasar esto a functions
                if not functions.create_unit_package(request, pckg):
                    return redirect('ListProductPackage')
                if functions.create_pckg_stock_control(request, pckg):
                    return redirect('ListProductPackage')
                else:
                    messages.error(
                        request, 'Error in the creation of the Stock Control')
            else:
                messages.success(
                    request, 'There are no units to create')
                return redirect('ListProductPackage')
    return redirect('ListProductPackage')


# ------------------MEASUREMENTS UNITS-----------------------------#

# ------------------------VIEWS------------------------------#
class ListMeasurementUnit(ListView):

    model = measurement_units
    template_name = 'measurement_units/views/ListMeasurementUnit.html'
    create_form = MeasurementUnitForm
    success_url = reverse_lazy('ListMeasurementUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nueva Unidad de Medida'
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)

# ----------------------------FUNCTIONS------------------------------#


class CreateMeasurementUnit(CreateView):
    model = measurement_units
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/CreateMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')


class EditMeasurementUnit(UpdateView):
    model = measurement_units
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/CreateMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')


class DeleteMeasurementUnit(DeleteView):
    model = measurement_units
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/DeleteMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')


# ----------------------STOCK MOVE MODEL----------------------------#
# --------------------------VIEWS-----------------------------------#


class ListStockMove(ListView):
    model = stock_move
    paginate_by = 20
    template_name = 'stock_move/views/ListStockMove.html'


class DetailStockMove(DetailView):
    model = stock_move
    template_name = 'stock_move/views/DetailStockMove.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        move_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        heading = '%s Detail' % move_id.code
        context['heading'] = heading
        return context


# ----------------------------------------FUNCTIONS----------------------------------------#

def function_create_move_unit(request):
    heading = 'Moviendo Unidad de Producto'
    title = 'Nuevo Movimiento'
    form = MoveUnitForm()
    if request.method == "POST":
        form = MoveUnitForm(request.POST)
    if form.is_valid():
        move = form.save(commit=False)
        if validations.validate_moves(request, move):
            return redirect('function_create_move_unit')
        if validations.validate_stock_control(request, move):
            return redirect('function_create_move_unit')
        if functions.create_stock_move(request, move):
            return redirect('ListStockMove')
    else:
        form = MoveUnitForm()
    return render(
        request,
        'stock_move/functions/function_create_move_unit.html',
        {"form": form,
         "heading": heading,
         "title": title})


def function_create_move_package(request):
    heading = 'Moviendo Paquete de Productos'
    title = 'Nuevo Movimiento'
    form = MovePackageForm()
    if request.method == "POST":
        form = MovePackageForm(request.POST)
    if form.is_valid():
        move = form.save(commit=False)
        if validations.validate_moves(request, move):
            return redirect('function_create_move_package')
        if validations.validate_stock_control(request, move):
            return redirect('function_create_move_package')
        if functions.create_stock_move(request, move):
            return redirect('ListStockMove')
    else:
        form = MovePackageForm()
    return render(
        request,
        'stock_move/functions/function_create_move_package.html',
        {"form": form,
         "heading": heading,
         "title": title})


# ---------------------------STOCK CONTROL-------------------------#
# -----------------------------VIEWS--------------------------------#


class ListStockControl(ListView):
    stock_control_model = stock_control
    paginate_by = 20
    template_name = 'stock_control/views/ListStockControl.html'
