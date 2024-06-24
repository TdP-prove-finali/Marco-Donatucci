from Model import device1234, device6, device7, device8, device9, device5, device10, device11, device12, device13, \
    device


#  il file device_DAO.py gestisce la creazione degli oggetti relativi ai dispositivi trovati


def getDevice(imei, selected_type, connection):
    """Crea gli oggetti Device e li include nel model"""
    imei = str(imei)
    connessione = connection.getConnection(imei)  # ricerca del dispositivo tramite codice identificativo univoco
    if connessione is not None:
        #  i tipi di dispositivi disponibili sono 14, con caratteristiche diverse, diversi tipi di comandi, 
        #  il metodo utilizza il costruttore della classe device relativa al numero del tipo di dispositivo
        if selected_type == '1' or selected_type == '2' or selected_type == '3' or selected_type == '4':
            try:
                result_device = device1234.Device1234(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'in', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=get_nested_value(connessione, ['prms', 'mileage', 'v']),
                    blocco=get_nested_value(connessione, ['prms', 'relay', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '5':
            try:
                result_device = device5.Device5(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'ign', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'odometer', 'v'], -1)),
                    blocco=get_nested_value(connessione, ['prms', 'digital_out', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '6':
            try:
                result_device = device6.Device6(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'ign', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'odometer', 'v'], -1)) / 1000
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '7':
            try:
                result_device = device7.Device7(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'io_239', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'io_16', 'v'], -1)) / 1000,
                    blocco=get_nested_value(connessione, ['prms', 'io_179', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '8':
            try:
                result_device = device8.Device8(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'io_239', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'io_87', 'v'], -1)) / 1000,
                    blocco=get_nested_value(connessione, ['prms', 'io_179', 'v']),
                    fuel_percentage=get_nested_value(connessione, ['prms', 'io_89', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'io_85', 'v']),
                    water_temp=float(get_nested_value(connessione, ['prms', 'io_115', 'v'], -1)) / 10,
                    blocco_carta=get_nested_value(connessione, ['prms', 'io_248', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '9':
            try:
                result_device = device9.Device9(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'io_239', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=get_nested_value(connessione, ['prms', 'tco_distance', 'v']),
                    fuel_percentage=get_nested_value(connessione, ['prms', 'io_87', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'io_88', 'v']),
                    water_temp=get_nested_value(connessione, ['prms', 'io_127', 'v']),
                    driver_id=get_nested_value(connessione, ['prms', 'tco_driver1_id', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '10':
            try:
                result_device = device10.Device10(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'io_239', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'io_87', 'v'], -1)) / 1000,
                    fuel_percentage=get_nested_value(connessione, ['prms', 'io_89', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'io_85', 'v']),
                    water_temp=float(get_nested_value(connessione, ['prms', 'io_115', 'v'], -1)) / 10,
                    blocco=get_nested_value(connessione, ['prms', 'io_179', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '11':
            try:
                result_device = device11.Device11(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'io_239', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=get_nested_value(connessione, ['prms', 'tco_distance', 'v']),
                    fuel_percentage=get_nested_value(connessione, ['prms', 'io_87', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'io_88', 'v']),
                    water_temp=get_nested_value(connessione, ['prms', 'io_127', 'v']),
                    driver_id=get_nested_value(connessione, ['prms', 'tco_driver1_id', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '12':
            try:
                result_device = device12.Device12(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'ign', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'can_total_dist_h', 'v'], -1)) / 10,
                    fuel_percentage=get_nested_value(connessione, ['prms', 'can_fuel_level_p', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'can_eng_rpm', 'v']),
                    water_temp=get_nested_value(connessione, ['prms', 'can_eng_cool_temp', 'v']),
                    blocco=get_nested_value(connessione, ['prms', 'dout_status', 'v']),
                    driver=get_nested_value(connessione, ['prms', 'id', 'v']),
                    km_gps=float(get_nested_value(connessione, ['prms', 'mileage', 'v'], -1))
                )
                return result_device
            except KeyError as e:
                return None
        elif selected_type == '13':
            try:
                result_device = device13.Device13(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'ign', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'can_total_distance', 'v'], -1)) / 10,
                    fuel_percentage=get_nested_value(connessione, ['prms', 'can_fuel_level_p', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'can_eng_rpm', 'v']),
                    water_temp=get_nested_value(connessione, ['prms', 'can_eng_cool_temp', 'v']),
                    driver_id=get_nested_value(connessione, ['prms', 'tco_driver1_id', 'v'])
                )
                return result_device
            except KeyError:
                return None
        elif selected_type == '14':
            try:
                result_device = device14.Device14(
                    uid=connessione.get('uid'),
                    itemId=connessione.get('id'),
                    name=connessione.get('nm'),
                    position=(
                        get_nested_value(connessione, ['pos', 'x']),
                        get_nested_value(connessione, ['pos', 'y'])
                    ),
                    device_status=connessione.get('act'),
                    object_status=get_nested_value(connessione, ['prms', 'ign', 'v']),
                    selected_type=selected_type,
                    battery=get_nested_value(connessione, ['prms', 'pwr_ext', 'v']),
                    total_km=float(get_nested_value(connessione, ['prms', 'can_total_distance', 'v'], -1)) / 10,
                    fuel_percentage=get_nested_value(connessione, ['prms', 'can_fuel_level_p', 'v']),
                    rpm=get_nested_value(connessione, ['prms', 'can_eng_rpm', 'v']),
                    water_temp=get_nested_value(connessione, ['prms', 'can_eng_cool_temp', 'v']),
                    driver=get_nested_value(connessione, ['prms', 'ibutton', 'v']),
                    blocco=get_nested_value(connessione, ['prms', 'dout_status', 'v']),
                    km_gps=float(get_nested_value(connessione, ['prms', 'mileage', 'v'], -1))
                )
                return result_device
            except KeyError:
                return None
    else:
        return None


def get_nested_value(dictionary, keys, default=None):
    """Ottieni un valore da un dizionario annidato."""
    for key in keys:
        dictionary = dictionary.get(key, default)
        if dictionary is default:
            break
    return dictionary
