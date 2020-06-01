from django.contrib import messages
from apps.warehouse.models import product_units
from apps.warehouse.models import stock_control
from apps.warehouse import functions


def validate_moves(request, move):
    '''
    Diferentes validaciones previas a la creación del movimiento
    '''
    #  sSi ocurre algún error en las validaciones, on_error cambiará a True
    #  La funcion devuelve el valor de on_error

    on_error = False

    if move.unit_id:
        item_move = move.unit_id
    elif move.package_id:
        item_move = move.package_id

    __VALID_MOVES__ = [
        'Ingress-Internal',
        'Internal-Internal',
        'Internal-Egress',
    ]

    __MOVE_TYPE__ = {
        'Ingress-Internal': 'Ingress',
        'Internal-Internal': 'Internal',
        'Internal-Egress': 'Egress',
    }

    validate_move = str(
        move.location_id.location_type + '-' +
        move.location_dest_id.location_type)

    msg_validate = {
        'origin_destination': 'La ubicación Destino no puede ser la misma '
                              'que el Origen, por favor verifique las '
                              'ubicaciones en el formulario.',
        'invalid_move': 'Movimiento Inválido: %s-%s '
                        % (move.location_id.name,
                           move.location_dest_id.name),
        'first_move': 'El primer movimiento de los paquetes debe ser '
                      'de tipo "Ingreso"',
        'origin_error': 'No puede mover desde %s '
                        'porque no hay disponibilidad en la ubicación %s. '
                        'Revise la disponibildad en las ubicaciones'
                        % (move.location_id.name,
                           move.location_id.name),
        'error_package_qty': 'Para mover paquetes, debe mover '
                             'la cantidad total disponible del paquete. '
                             'Actualmente el paquete tiene %s Piezas '
                             'y usted intenta mover %s piezas. Por favor corrija'
                             % (move.package_id.pieces if move.package_id
                                else None, move.pieces),
        'fixed_ammount': 'Esta unidad debe moverse siempre '
                         'con la cantidad fija de %s %s'
                         % (move.unit_id.quantity if move.unit_id
                            else None,
                            item_move.product_id.measure_id.abbreviation),
        'error_quantity': 'No hay %s %s disponible. '
                          'La cantidad disponibile de %s es de %s %s'
                          % (move.quantity if move.unit_id
                             else None,
                             item_move.product_id.measure_id.abbreviation,
                             item_move.code, move.quantity if move.unit_id
                             else None,
                             item_move.product_id.measure_id.abbreviation),
    }

    if validate_move not in __VALID_MOVES__:
        on_error = True
        messages.error(request, msg_validate['invalid_move'])
        return on_error
    else:
        move.move_type = __MOVE_TYPE__[validate_move]

    if move.location_dest_id == move.location_id:
        on_error = True
        messages.error(
            request, msg_validate['origin_destination'])
        return on_error

    if move.package_id:
        if not move.package_id.location_id \
                and move.location_id.location_type != 'Ingress':
            on_error = True
            messages.error(request, msg_validate['first_move'])
            return on_error

        elif move.package_id.location_id != move.location_id \
                and move.location_id.location_type != 'Ingress':
            on_error = True
            messages.error(request, msg_validate['origin_error'])
            return on_error

        if move.package_id.pieces:
            if move.package_id.pieces != move.pieces:
                on_error = True
                messages.error(request, msg_validate['error_package_qty'])
                return on_error

    if move.unit_id:
        if not move.unit_id.location_id:
            if move.location_id.location_type != 'Ingress':
                on_error = True
                messages.error(request, msg_validate['first_move'])
                return on_error
        if move.unit_id.fixed_ammount \
                and move.quantity != move.unit_id.quantity \
                and move.location_id.location_type != 'Ingress':
            on_error = True
            messages.error(request, msg_validate['fixed_ammount'])
            return on_error
        if move.unit_id and move.unit_id.quantity and move.quantity < 0.0:
            if move.unit_id.quantity < move.quantity:
                on_error = True
                messages.error(request, msg_validate['error_quantity'])
                return on_error
    return on_error


def validate_stock_control(request, move):
    '''
    Diferentes validaciones previas a la creación del
    Control de Stock
    Si ocurre algún error en las validaciones, on_error cambiará a True
    La funcion devuelve el valor de on_error
    '''
    on_error = False
    stock_control_data = {
        'origin_data': False,
        'dest_data': False,
        }
    '''
    La lista unit_list se utiliza para almacenar
    Los ids de las unidades de producto, e iterar sobre ellos
    Tanto para movimientos de unidades indivuales: una sola iteración
    o paquetes: iteraciónes tantas unidades agrupe el paquete
    '''
    unit_list = []
    if move.unit_id:
        measure = move.unit_id.product_id.measure_id.abbreviation
        unit_list.append(move.unit_id)
    if move.package_id:
        measure = move.package_id.product_id.measure_id.abbreviation
        unit_ids = product_units.objects.filter(package_id=move.package_id)
        for unit_id in unit_ids:
            unit_list.append(unit_id)
    for unit_id in unit_list:
        if unit_id.stock_ctrl:
            if move.location_id.location_type != 'Ingress':
                stck_ctrl_origin = stock_control.objects.filter(
                    unit_id=unit_id.id, location_id=move.location_id)
                if not stck_ctrl_origin:
                    on_error = True
                    stock_control_error = \
                        'No puede mover la unidad desde la ubicación ' \
                        '%s porque la unidad no tienen Stock disponible ' \
                        'en esa ubicación. ' \
                        'Revise el Stock disponible y corrija. ' \
                        % (move.location_id)
                    messages.error(request, stock_control_error)
                else:
                    for origin_data in stck_ctrl_origin:
                        stock_control_data['origin_data'] = origin_data
                        if origin_data.quantity < move.quantity \
                                and move.unit_id:
                            on_error = True
                            stock_control_error = \
                                'No hay Stock disponible en %s. ' \
                                'Está tratando de mover %s %s pero la ' \
                                'cantidad disponible en %s es de %s. ' \
                                'Por favor Corrija ' \
                                % (move.location_id.name,
                                   move.quantity,
                                   measure,
                                   origin_data.location_id.name,
                                   origin_data.quantity)
                            messages.error(request, stock_control_error)
                        else:
                            stck_ctrl_dest = stock_control.objects.filter(
                                unit_id=unit_id.id,
                                location_id=move.location_dest_id)
                            if stck_ctrl_dest:
                                for dest_data in stck_ctrl_dest:
                                    stock_control_data['dest_data'] = dest_data
                            if not functions.create_stock_control(
                                    request, stock_control_data,
                                    unit_id, move):
                                messages.error(
                                    request,
                                    'Error creando el Control de Stock')
            else:
                on_error = True
                ingress_error = \
                    'Esta unidad ya tuvo un ingreso, por favor corrija'
                messages.error(request, ingress_error)
        else:
            if not functions.create_stock_control(
                    request, stock_control_data, unit_id, move):
                messages.error(
                    request, 'Error en la creación del Control de Stock')
    return on_error
