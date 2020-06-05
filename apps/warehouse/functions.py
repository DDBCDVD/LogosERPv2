from django.contrib import messages
from apps.warehouse.models import StockControl
from apps.warehouse.models import ProductUnit
from apps.warehouse.models import ProductPackage


def create_unit_package(request, pckg):
    units_create = False
    for qty in range(int(pckg.pieces)):
        ProductUnit.objects.create(
            name=str(pckg.product_id.name + ' ' + pckg.code),
            measure=str(pckg.product_id.measure_id.name),
            product_id=pckg.product_id,
            location_id_id=pckg.location_id.id,
            package_id=pckg,
            fixed_ammount=pckg.fixed_ammount)
    pckg.units_created = True
    pckg.save()
    msg = '%s Unidades Creadas' % pckg.pieces
    messages.success(request, msg)
    units_create = True
    return units_create


def create_pckg_stock_control(request, pckg):
    stock_control_created = False
    unit_ids = ProductUnit.objects.filter(package_id=pckg.id)
    if unit_ids:
        for unit_id in unit_ids:
            StockControl.objects.create(
                quantity=int(pckg.unit_qty),
                unit_id=unit_id,
                location_id=pckg.location_id
            )
            unit_id.quantity = int(pckg.unit_qty)
            unit_id.stock_ctrl = True
            unit_id.first_move = True
            unit_id.save()
        stock_control_created = True
        msg = 'Controles de Stock creados para %s unidades' % len(unit_ids)
        messages.success(request, msg)
    return stock_control_created


def create_stock_move(request, move):
    location_dest_id = move.location_dest_id
    location_id = move.location_id
    '''
    Si el movimiento se ejecuta sin problemas,
    moved cambiará a True.
    La funcion devuelve el valor de moved
    '''
    moved = False

    if move.package_id:
        package_id = move.package_id.id
        product_package = ProductPackage.objects.get(id=package_id)
        product_package.location_id_id = location_dest_id
        product_package.pieces = move.pieces
        product_package.first_move = True
        product_package.save()
        unit_ids = ProductUnit.objects.filter(package_id=package_id)
        if unit_ids:
            for unit_id in unit_ids:
                unit_id.location_id_id = location_dest_id
                unit_id.save()
        move.save()
        msg = '%s Piezas Movidas con Éxito!' % (
            move.pieces)
        messages.success(request, msg)
        moved = True

    if move.unit_id:
        unit_id = move.unit_id.id
        product_unit = ProductUnit.objects.get(id=unit_id)
        product_unit.location_id_id = location_dest_id
        product_unit.location_from_id_id = location_id
        product_unit.save()
        move.save()
        msg = '%s %s Movido con Éxito!' % (
            move.quantity,
            move.unit_id.product_id.measure_id.abbreviation)
        messages.success(request, msg)
        moved = True
    return moved


def create_stock_control(request, stock_control_data, unit_id, move):
    '''
    Esta funcion crea los controles de Stock individual a cada unidad.
    La variable stock_control_data es un dicconario que
    contiene la informacion de stock de las unidades: Ubicacion y Cantidades.
    Con esta informacion se crean los Controles de Stock dependiendo
    de la información que contenga o no el stock_control_data.
    También se calculan aquí los saldos de las unidades:
    El saldo total y el saldo indivdual por ubicación para
    cada unidad de producto
    Si el control de stock se crea sin problemas,
    'stock_control_created' cambiará a True
    La funcion devuelve el valor de stock_control_created
    '''
    stock_control_created = False
    origin_data = stock_control_data['origin_data']
    dest_data = stock_control_data['dest_data']

    if not origin_data:
        '''
        Este bloque crea un Control de Stock nuevo
        ya que no existe uno para la unidad
        en la ubicacion Origen.
        Esto aplica sólo para los movimientos de tipo Ingreso.
        Calcula tambien los saldos respectivos y es aquí donde se
        ingresa la cantidad total de la unidad de producto.
        '''
        if move.unit_id:
            # Calcula el saldo de la unidad en el almacén
            move.prev_qty = unit_id.quantity
            move.balance = move.unit_id.quantity + move.quantity
            move.prev_qty_origin = None
            move.balance_origin = None
            move.prev_qty_dest = unit_id.quantity
            move.balance_dest = move.unit_id.quantity + move.quantity

            StockControl.objects.create(
                    quantity=move.quantity,
                    unit_id=unit_id,
                    location_id=move.location_dest_id)
            unit_id.quantity = move.quantity
            unit_id.stock_ctrl = True
            unit_id.first_move = True
            unit_id.save()
            msg = 'Control de Stock creado para la unidad %s' % unit_id.code
            messages.success(request, msg)
            stock_control_created = True

    elif origin_data:
        '''
        Este bloque valida si el movimiento es Interno o Egreso.
        Crea o actualiza el Control de Stock para la unidad
        en la ubicacion Destino, dependiendo del caso.
        Esto aplica para los movimientos de tipo Interno:
        Si no hay Control de Stock destino para la unidad
        (if not dest_data:), este se crea, de lo contrario
        (elif dest_data:), sólo se actualiza.
        Se suma al stock control destino la cantidad
        definida en el movimiento y a su vez esta cantidad se resta
        al Control de Stock origen.
        Si el movimiento es INTERNO:
            La cantidad total de la unidad no se modifica.
        Si el movimiento es EGRESO:
            Se resta la catidad del movimiento a la cantidad total de la unidad
        En ambos casos se actualiza el control de Stock Origen,
        Si el control de Stock origen queda en 0, entonces es borrado.
        Calcula tambien los saldos respectivos.
        '''

        if move.location_dest_id.location_type == 'Internal':
            if not dest_data:
                '''
                Si no hay Control de Stock destino para la unidad
                '''

                if move.package_id:
                    origin_data.quantity = \
                        origin_data.quantity - origin_data.quantity
                elif move.unit_id:
                    # Calcula el saldo de la unidad en el almacén
                    move.prev_qty = unit_id.quantity
                    move.balance = move.unit_id.quantity
                    move.prev_qty_origin = origin_data.quantity
                    move.balance_origin = origin_data.quantity - move.quantity
                    move.prev_qty_dest = 0.0
                    move.balance_dest = 0.0 + move.quantity

                    origin_data.quantity = origin_data.quantity - move.quantity

                    origin_data.save()
                    if origin_data.quantity == 0.0:
                        origin_data.delete()
                    StockControl.objects.create(
                        quantity=move.quantity,
                        unit_id=unit_id,
                        location_id=move.location_dest_id)
                    msg = 'Movimiento  interno creado para %s unidad' \
                          % unit_id.code
                    messages.success(request, msg)
                    stock_control_created = True

            elif dest_data:
                '''
                Si hay Control de Stock destino para la unidad
                '''
                if move.package_id:
                    dest_data.quantity = origin_data.quantity
                    origin_data.quantity = \
                        origin_data.quantity - origin_data.quantity
                elif move.unit_id:
                    # Calcula el saldo de la unidad en el almacén
                    move.prev_qty = unit_id.quantity
                    move.balance = move.unit_id.quantity
                    move.prev_qty_origin = origin_data.quantity
                    move.balance_origin = origin_data.quantity - move.quantity
                    move.prev_qty_dest = dest_data.quantity
                    move.balance_dest = dest_data.quantity + move.quantity

                    dest_data.quantity = dest_data.quantity + move.quantity
                    origin_data.quantity = origin_data.quantity - move.quantity

                origin_data.save()
                dest_data.save()
                if origin_data.quantity == 0.0:
                    origin_data.delete()
                msg = 'Movimiento  interno creado para %s unidad' \
                      % unit_id.code
                messages.success(request, msg)
                stock_control_created = True

        elif move.location_dest_id.location_type == 'Egress':
            if move.unit_id:
                # Calcula el saldo de la unidad en el almacén
                move.prev_qty = unit_id.quantity
                move.balance = move.unit_id.quantity - move.quantity
                move.prev_qty_origin = origin_data.quantity
                move.balance_origin = origin_data.quantity - move.quantity
                move.prev_qty_dest = None
                move.balance_dest = None

            if move.package_id:
                quantity = origin_data.quantity
                origin_data.quantity = origin_data.quantity - quantity
            elif move.unit_id:
                quantity = origin_data.quantity - move.quantity
                origin_data.quantity = origin_data.quantity - move.quantity
            origin_data.save()
            unit_id.quantity = unit_id.quantity - move.quantity
            unit_id.save()
            if origin_data.quantity == 0.0:
                origin_data.delete()
                if unit_id.package_id:
                    package_id = ProductPackage.objects.get(
                        id=unit_id.package_id.id)
                    package_id.unit_qty = package_id.unit_qty - 1
                    package_id.save()
            stock_control_created = True
    return stock_control_created
