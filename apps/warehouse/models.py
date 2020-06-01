from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class measurement_units(models.Model):

    __AUTOCODE__ = 'MSRE'

    code = models.CharField(
        verbose_name="Código",
        max_length=100, unique=True)
    name = models.CharField(
        max_length=30,
        verbose_name="Nombre")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    unit_qty = models.PositiveIntegerField(
        verbose_name="Factor de Medida",
        default=0.0)
    abbreviation = models.CharField(
        verbose_name="Abbreviación",
        max_length=5)
    date_created = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Creación")
    date_modify = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        db_table = 'measurement_units'
        ordering = ['code']

    @receiver(post_save, sender='warehouse.measurement_units')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))


class products(models.Model):

    __AUTOCODE__ = 'PRD'

    code = models.CharField(
        verbose_name="Código",
        max_length=100,
        unique=True)
    name = models.CharField(
        max_length=30, verbose_name="Nombre")
    active = models.BooleanField(
        default=True, verbose_name="Activo")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    measure_id = models.ForeignKey(
        measurement_units,
        verbose_name="Unidad de Medida",
        on_delete=models.CASCADE)
    measure_qty = models.PositiveIntegerField(
        verbose_name="Factor de Cantidad",
        default=0.0)
    date_created = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Creación")
    date_modify = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return str(self.code + ' ' + self.name)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'products'
        ordering = ['code']

    @receiver(post_save, sender='warehouse.products')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))

    # def save(self, instance, **kwargs):
    #     while kwargs.get('created') == False:
    #         code_str = str(self.__AUTOCODE__)
    #     code_str = str(self.__AUTOCODE__ + str(instance.id))
    #     self.code = code_str
    #     super().save(*kwargs)


class stock_location(models.Model):

    __AUTOCODE__ = 'STCKLO'

    ingress = 'Ingress'
    egress = 'Egress'
    internal = 'Internal'
    null = 'Null'

    TYPE_CHOICES = [
        (null, 'Null'),
        (ingress, 'Ingress'),
        (egress, 'Egress'),
        (internal, 'Internal'),
    ]
    location_type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
        default=null,
    )
    code = models.CharField(
        verbose_name="Código",
        max_length=100, unique=True)
    name = models.CharField(
        max_length=30,
        verbose_name="Nombre")
    active = models.BooleanField(
        default=True, verbose_name="Activo")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    date_created = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Creación")
    date_modify = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        db_table = 'stock_location'
        ordering = ['name']

    @receiver(post_save, sender='warehouse.stock_location')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))


class products_package(models.Model):

    __AUTOCODE__ = 'PCKG'

    code = models.CharField(
        verbose_name="Código",
        max_length=100)
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripcion")
    pieces = models.PositiveIntegerField(
        verbose_name="Piezas", null=True,
        blank=True)
    units_created = models.BooleanField(
        default=False)
    unit_qty = models.FloatField(
        verbose_name="Cantidad de Unidades",
        default=0.0)
    product_id = models.ForeignKey(
        products, verbose_name="Producto",
        on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        stock_location,
        verbose_name="Ubicación", null=True, blank=True,
        on_delete=models.CASCADE)
    fixed_ammount = models.BooleanField(
        verbose_name="Fijar Cantidad",
        default=False)
    first_move = models.BooleanField(
        verbose_name="Primer Movimiento",
        default=False)
    date_created = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de Creación")
    date_modify = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        if self.location_id:
            name_location = str(self.location_id.name)
        else:
            name_location = ''
        return str(self.code + ' ' + name_location)

    class Meta:
        verbose_name = 'Paquete de Productos'
        verbose_name_plural = 'Paquetes de Productos'
        db_table = 'products_package'
        ordering = ['code']

    @receiver(post_save, sender='warehouse.products_package')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))


class product_units(models.Model):

    __AUTOCODE__ = 'PRDUNT'

    code = models.CharField(
        verbose_name="Código", max_length=100,
        unique=True)
    name = models.CharField(
        max_length=30, verbose_name="Nombre")
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Descripción")
    quantity = models.FloatField(
        verbose_name="Cantidad",
         default=0.0)
    pieces = models.PositiveIntegerField(
        verbose_name="Piezas", default=0.0)
    product_id = models.ForeignKey(
        products, verbose_name="Producto",
        on_delete=models.CASCADE)
    measure = models.CharField(
        verbose_name="Medida", max_length=30)
    package_id = models.ForeignKey(
        products_package,
        null=True, blank=True, verbose_name="Paquete",
        on_delete=models.SET_NULL)
    location_id = models.ForeignKey(
        stock_location,
        verbose_name="Ubicación", null=True,
        blank=True, on_delete=models.CASCADE)
    stock_ctrl = models.BooleanField(
        default=False)
    fixed_ammount = models.BooleanField(
        verbose_name="Fijar Cantidad", default=False)
    first_move = models.BooleanField(
        verbose_name="Primer Movimiento", default=False)
    date_created = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de Creación")
    date_modify = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return str(
            self.name
            + ' ' + self.code + ' ' + str(self.quantity) + ' '
            + self.product_id.measure_id.abbreviation)

    class Meta:
        verbose_name = 'Unidad de Producto'
        verbose_name_plural = 'Unidades de Producto'
        db_table = 'product_units'
        ordering = ['code']

    @receiver(post_save, sender='warehouse.product_units')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            autocode = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))


class stock_move(models.Model):

    __AUTOCODE__ = 'MOVE'

    code = models.CharField(
        verbose_name="Código", max_length=100,
        unique=True)
    note = models.TextField(
        verbose_name="Notas")
    description = models.TextField(
        verbose_name="Descripcion")
    pieces = models.IntegerField(
        verbose_name="Piezas",
        default=0.0)
    quantity = models.FloatField(
        verbose_name="Cantidad",
        default=0.0)
    prev_qty = models.FloatField(
        verbose_name="Cantidad previa de la Unidad",
        default=0.0)
    balance = models.FloatField(
        verbose_name="Saldo total de la Unidad",
        default=0.0)
    prev_qty_origin = models.FloatField(
        null=True, blank=True,
        verbose_name="Cantidad previa en el origen",
        default=0.0)
    balance_origin = models.FloatField(
        null=True, blank=True,
        verbose_name="Saldo nuevo en el origen",
        default=0.0)
    prev_qty_dest = models.FloatField(
        null=True, blank=True,
        verbose_name="Cantidad previa en el Destino",
        default=0.0)
    balance_dest = models.FloatField(
        null=True, blank=True,
        verbose_name="Saldo nuevo en el Destino",
        default=0.0)
    unit_id = models.ForeignKey(
        product_units, null=True, blank=True,
        verbose_name="Unidad de Producto",
        on_delete=models.CASCADE)
    package_id = models.ForeignKey(
        products_package, null=True, blank=True,
        verbose_name="Paquetes", on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        stock_location, on_delete=models.CASCADE)
    location_dest_id = models.ForeignKey(
        stock_location, on_delete=models.CASCADE, related_name='+')
    date = models.DateTimeField(
        verbose_name="Fecha", default=datetime.now)
    move_type = models.CharField(
        verbose_name="Tipo de Movimiento", max_length=100)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        db_table = 'stock_move'
        ordering = ['code']

    @receiver(post_save, sender='warehouse.stock_move')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))


class stock_control(models.Model):

    __AUTOCODE__ = 'STKCTRL'

    code = models.CharField(
        verbose_name="Codigo", max_length=100,
        unique=True)
    pieces = models.IntegerField(
        verbose_name="Piezas", default=0.0)
    quantity = models.FloatField(
        verbose_name="Cantidad",
        default=0.0)
    unit_id = models.ForeignKey(
        product_units, null=True, blank=True,
        verbose_name="Unidad de Producto",
        on_delete=models.CASCADE,default=0.0)
    unit_id = models.ForeignKey(product_units,
    null=True, blank=True,
    verbose_name="Unidad de Producto",
    on_delete=models.CASCADE)
    location_id = models.ForeignKey(
        stock_location, on_delete=models.CASCADE)
    date = models.DateField(
        verbose_name="Fecha", auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Control de Stock'
        verbose_name_plural = 'Controles de Stock'
        db_table = 'stock_control'
        ordering = ['code']

    @receiver(post_save, sender='warehouse.stock_control')
    def set_auto_code(sender, instance, **kwargs):
        if kwargs.get('created'):
            code = sender.objects.filter(id=instance.id).update(
                code=instance.__AUTOCODE__ + str(instance.id))