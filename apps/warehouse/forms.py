from django import forms
# from bootstrap_modal_forms.forms import BSModalForm
from apps.warehouse.models import products
from apps.warehouse.models import stock_location
from apps.warehouse.models import product_units
from apps.warehouse.models import products_package
from apps.warehouse.models import measurement_units
from apps.warehouse.models import stock_move


class ProductForm(forms.ModelForm):


    class Meta:
        model = products

        fields = [
            'name',
            'active',
            'measure_id',
            'description',
            ]
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'measure_id': 'Unidad de Medida',
            'active': 'Activo  ?',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class':'form-control', 'placeholder':"Nombre Producto"}),
            'active': forms.CheckboxInput(),
            'measure_id': forms.Select(
                attrs={'class':'form-control select2'}),
            'description': forms.Textarea(
                attrs={'class':'form-control', 'placeholder':"Añadir Descripción"}),

        }


class ProductUnitForm(forms.ModelForm):

    class Meta:
        model = product_units

        fields = [
            'name',
            'product_id',
            'fixed_ammount',
            'description',
            ]
        labels = {
            'name': 'Nombre',
            'product_id': 'Producto',
            'fixed_ammount': 'Cantidad Fija',
            'description': 'Descripción',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Nombre de la Unidad"}),
            'product_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'fixed_ammount': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Añadir una Descripción'}),
        }


class StockLocationForm(forms.ModelForm):

    class Meta:
        model = stock_location

        fields = [
            'name',
            'active',
            'location_type',
            'description',
            ]
        labels = {
            'name': 'Nombre',
            'location_type': 'Tipo de Ubicación',
            'active': 'Activo  ?',
            'description': 'Descripción',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ubicación'}),
            'active': forms.CheckboxInput(),
            'location_type': forms.Select(
                attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Añadir Descripción'}),
        }


class ProductPackageForm(forms.ModelForm):

    class Meta:
        model = products_package

        fields = [
            'product_id',
            'unit_qty',
            'fixed_ammount',
            'description',
            ]
        labels = {

            'product_id': 'Producto',
            'unit_qty': 'Cantidad por Unidad',
            'fixed_ammount': 'Cantidad fija por Unidad',
            'description': 'Descripción',
        }
        widgets = {
            'product_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'unit_qty': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'fixed_ammount': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir Descripción'}),
        }


class MeasurementUnitForm(forms.ModelForm):

    class Meta:
        model = measurement_units

        fields = [
            'name',
            'unit_qty',
            'abbreviation',
            'description',
        ]
        labels = {
            'name': 'Nombre',
            'unit_qty': 'Factor de la Unidad',
            'abbreviation': 'Abreviatura',
            'description': 'Descripción',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Nombre unidad de Medida'}),
            'unit_qty': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Kg., Lt, m2...'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir Descripción'}),
        }


class MovePackageForm(forms.ModelForm):

    class Meta:
        model = stock_move

        fields = [
            'note',
            'pieces',
            'package_id',
            'location_id',
            'location_dest_id',
            'description',
            ]

        labels = {
            'note': 'Notas',
            'pieces': 'Piezas',
            'package_id': 'Paquete',
            'location_id': 'Origen',
            'location_dest_id': ' Destino',
            'description': 'Descripción',
        }

        widgets = {
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
            'pieces': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'package_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'location_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'location_dest_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Agregue una Descripción'}),
        }


class MoveUnitForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # for field in self.visible_fields():
    #     #     field.widget.attrs['class'] = 'form-control'
    #         # field.widget.attrs['autocomplete'] = 'off'
    #     self.fields['note'].widget.attrs['autofocus'] = True

    unit_id = forms.ModelChoiceField(
        product_units.objects.exclude(
            quantity__lte=0.000001,
            first_move=True)
        )

    class Meta:
        model = stock_move

        fields = [
            'note',
            'quantity',
            'unit_id',
            'location_id',
            'location_dest_id',
            'description',
        ]

        labels = {
            'note': 'Notas',
            'quantity': 'Cantidad',
            'unit_id': 'Unidad de Producto',
            'location_id': 'Origen',
            'location_dest_id': 'Destino',
            'description': 'Descripción',
        }

        widgets = {
            'note': forms.TextInput(
                attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'unit_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'location_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'location_dest_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Agregue una Descripción'}),
        }