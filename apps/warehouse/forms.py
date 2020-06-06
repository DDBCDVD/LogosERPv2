from django import forms
# from bootstrap_modal_forms.forms import BSModalForm
from apps.warehouse.models import Product
from apps.warehouse.models import StockLocation
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage
from apps.warehouse.models import MeasurementUnit
from apps.warehouse.models import StockMove


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product

        fields = [
            'name',
            'active',
            'measure_id',
            'description',
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': "Nombre Producto"}),
            'active': forms.CheckboxInput(),
            'measure_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': "Añadir Descripción"}),

        }


class ProductUnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductUnit

        fields = [
            'name',
            'product_id',
            'fixed_ammount',
            'description',
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': "Nombre de la Unidad"}),
            'product_id': forms.Select(
                attrs={'class': 'form-control select2'}),
            'fixed_ammount': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir una Descripción'}),
        }


class StockLocationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = StockLocation

        fields = [
            'name',
            'location_type',
            'active',
            'description',
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Ubicación'}),
            'location_type': forms.Select(
                attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(),
            'description': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Añadir Descripción'}),
        }


class ProductPackageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['unit_qty'].widget.attrs['autofocus'] = True

    class Meta:
        model = ProductPackage

        fields = [
            'product_id',
            'unit_qty',
            'fixed_ammount',
            'description',
            ]
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = MeasurementUnit

        fields = [
            'name',
            'unit_qty',
            'abbreviation',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Nombre unidad de Medida'}),
            'unit_qty': forms.NumberInput(),
            'abbreviation': forms.TextInput(
                attrs={'placeholder': 'Kg., Lt, m2...'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Añadir Descripción'}),
        }


class MovePackageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['note'].widget.attrs['autofocus'] = True

    class Meta:
        model = StockMove

        fields = [
            'note',
            'pieces',
            'package_id',
            'location_id',
            'location_dest_id',
            'description',
            ]
        widgets = {
            'note': forms.TextInput(),
            'pieces': forms.NumberInput(),
            'package_id': forms.Select(),
            'location_id': forms.Select(),
            'location_dest_id': forms.Select(),
            'description': forms.Textarea(
                attrs={'placeholder': 'Agregue una Descripción'}),
        }


class MoveUnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['note'].widget.attrs['autofocus'] = True

    unit_id = forms.ModelChoiceField(
        ProductUnit.objects.exclude(
            quantity__lte=0.000001,
            first_move=True)
        )

    class Meta:
        model = StockMove

        fields = [
            'note',
            'quantity',
            'unit_id',
            'location_id',
            'location_dest_id',
            'description',
        ]
        widgets = {
            'note': forms.TextInput(),
            'quantity': forms.NumberInput(),
            'unit_id': forms.Select(),
            'location_id': forms.Select(),
            'location_dest_id': forms.Select(),
            'description': forms.Textarea(
                attrs={'placeholder': 'Agregue una Descripción'}),
        }