from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import DeleteView, DetailView
#  from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy
import apps.warehouse.validations as validations
import apps.warehouse.functions as functions
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit
from apps.warehouse.models import StockMove
from apps.warehouse.models import StockControl
from apps.warehouse.forms import ProductForm
from apps.warehouse.forms import StockLocationForm
from apps.warehouse.forms import ProductUnitForm
from apps.warehouse.forms import ProductPackageForm
from apps.warehouse.forms import MeasurementUnitForm
from apps.warehouse.forms import MovePackageForm
from apps.warehouse.forms import MoveUnitForm


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

    model = Product
    create_form = ProductForm
    template_name = 'products/views/ListProduct.html'
    success_url = reverse_lazy('ListProduct')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nuevo Producto'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateProduct'),
                      'text': 'Crear Nuevo Producto'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProduct(DetailView):
    model = ProductUnit
    template_name = 'products/views/DetailProduct.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        unit_ids = ProductUnit.objects.filter(product_id=product_id)
        package_ids = ProductPackage.objects.filter(product_id=product_id)
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
    model = Product
    form_class = ProductForm
    template_name = 'products/functions/CreateProduct.html'
    success_url = reverse_lazy('ListProduct')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditProduct(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/functions/CreateProduct.html'
    success_url = reverse_lazy('ListProduct')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteProduct(DeleteView):
    model = Product
    form_class = ProductForm
    template_name = 'products/functions/DeleteProduct.html'
    success_url = reverse_lazy('ListProduct')


# --------------------PRODUCT UNIT MODEL----------------------------#

# ------------------------VIEWS------------------------------#


class ListProductUnit(ListView):

    model = ProductUnit
    create_form = ProductUnitForm
    template_name = 'product_units/views/ListProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nueva Unidad de Producto'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateProductUnit'),
                      'text': 'Crear Nueva Unidad'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProductUnit(DetailView):
    model = ProductUnit
    template_name = 'product_units/views/DetailProductUnit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        move_ids = StockMove.objects.filter(unit_id=unit_id)
        heading = 'Detalle %s' % unit_id.code
        context['heading'] = heading
        context['move_heading'] = 'Movimientos'
        context['item_type'] = 'Unit'
        if move_ids:
            context['move_ids'] = move_ids
        if unit_id.package_id:
            print(unit_id.package_id.code)
            move_pckg_ids = StockMove.objects.filter(
                package_id=unit_id.package_id.id)
            if move_pckg_ids:
                context['move_pckg_ids'] = move_pckg_ids
                context['pckg_moves'] = 'Movimientos del Paquete'
        else:
            print('No hay paquete asociado')
        return context


# ------------------------FUNCTIONS------------------------------#

class CreateProductUnit(CreateView):
    model = ProductUnit
    addform = ProductForm
    form_class = ProductUnitForm
    template_name = 'product_units/functions/CreateProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditProductUnit(UpdateView):
    model = ProductUnit
    form_class = ProductUnitForm
    template_name = 'product_units/functions/CreateProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')


class DeleteProductUnit(DeleteView):
    model = ProductUnit
    form_class = ProductUnitForm
    template_name = 'product_units/functions/DeleteProductUnit.html'
    success_url = reverse_lazy('ListProductUnit')


# --------------------STOCK LOCATION MODEL--------------------------#

# ------------------------VIEWS------------------------------#
class ListStockLocation(ListView):

    model = StockLocation
    template_name = 'stock_location/views/ListStockLocation.html'
    create_form = StockLocationForm
    success_url = reverse_lazy('ListStockLocation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nueva Ubicación'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateStockLocation'),
                      'text': 'Crear Nueva Ubicación'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailStockLocation(DetailView):
    model = StockLocation
    template_name = 'stock_location/views/DetailStockLocation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        stkctrl_ids = stock_control.objects.filter(location_id=location_id)
        pckg_ids = ProductPackage.objects.filter(location_id=location_id)
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
    model = StockLocation
    form_class = StockLocationForm
    template_name = 'stock_location/functions/CreateStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditStockLocation(UpdateView):

    model = StockLocation
    form_class = StockLocationForm
    template_name = 'stock_location/functions/CreateStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteStockLocation(DeleteView):
    model = StockLocation
    form_class = StockLocationForm
    template_name = 'stock_location/functions/DeleteStockLocation.html'
    success_url = reverse_lazy('ListStockLocation')


# -----------------------PRODUCT PACKAGE MODEL-----------------------#

# ------------------------VIEWS------------------------------#
class ListProductPackage(ListView):

    model = ProductPackage
    template_name = 'products_package/views/ListProductPackage.html'
    create_form = ProductPackageForm
    success_url = reverse_lazy('ListProductPackage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        context['headmodal'] = 'Nuevo Paquete'
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateProductPackage'),
                      'text': 'Crear Nuevo Paquete'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)


class DetailProductPackage(DetailView):
    model = ProductPackage
    template_name = 'products_package/views/DetailProductPackage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.model.objects.get(pk=self.kwargs.get('pk'))
        move_ids = StockMove.objects.filter(package_id=package_id.id)
        unit_ids = ProductUnit.objects.filter(package_id=package_id.id)

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
    model = ProductPackage
    form_class = ProductPackageForm
    template_name = 'products_package/functions/CreateProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditProductPackage(UpdateView):
    model = ProductPackage
    form_class = ProductPackageForm
    template_name = 'products_package/functions/CreateProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')


class DeleteProductPackage(DeleteView):
    model = ProductPackage
    form_class = ProductPackageForm
    template_name = 'products_package/functions/DeleteProductPackage.html'
    success_url = reverse_lazy('ListProductPackage')


def create_unit_package(request, pk):
    '''
    Create multiple product_unit from this package

    '''
    package = ProductPackage.objects.filter(id=pk)
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

    model = MeasurementUnit
    template_name = 'measurement_units/views/ListMeasurementUnit.html'
    create_form = MeasurementUnitForm
    success_url = reverse_lazy('ListMeasurementUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = self.create_form
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateMeasurementUnit'),
                      'text': 'Crear nueva Medida'},
        }
        context['create_forms'] = create_forms
        return context

    def post(self, request, *args, **kwargs):
        create_form = self.create_form(request.POST)
        if create_form.is_valid():
            create_form.save()
            return HttpResponseRedirect(self.success_url)

# ----------------------------FUNCTIONS------------------------------#


class CreateMeasurementUnit(CreateView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/CreateMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class EditMeasurementUnit(UpdateView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/CreateMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteMeasurementUnit(DeleteView):
    model = MeasurementUnit
    form_class = MeasurementUnitForm
    template_name = 'measurement_units/functions/DeleteMeasurementUnit.html'
    success_url = reverse_lazy('ListMeasurementUnit')


# ----------------------STOCK MOVE MODEL----------------------------#
# --------------------------VIEWS-----------------------------------#


class ListStockMove(ListView):
    model = StockMove
    template_name = 'stock_move/views/ListStockMove.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_forms = {
            'form1': {'button_create': reverse_lazy('function_create_move_unit'),
                      'text': 'Mover Unidad'},
            'form2': {'button_create': reverse_lazy('function_create_move_package'),
                      'text': 'Mover Paquete'}

        }
        context['create_forms'] = create_forms
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = StockMove.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DetailStockMove(DetailView):
    model = StockMove
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
    model = StockControl
    paginate_by = 20
    template_name = 'stock_control/views/ListStockControl.html'
