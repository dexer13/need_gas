from datetime import datetime
from django.utils.timezone import make_aware
from ..core import MapSimulator
from ..models import Location, GasStation, Service, Driver, Customer


def get_drivers_data():
    return [
        {'name': 'Juan', 'identification': '111', 'x': 20, 'y': 10,
         'is_busy': True},
        {'name': 'Angie', 'identification': '222', 'x': 15, 'y': 20,
         'is_busy': False},
        {'name': 'Camilo', 'identification': '333', 'x': 12, 'y': 14,
         'is_busy': False},
        {'name': 'Daniela', 'identification': '444', 'x': 9, 'y': 10,
         'is_busy': True},
        {'name': 'Sebastian', 'identification': '555', 'x': 22, 'y': 17,
         'is_busy': True},
        {'name': 'Andrea', 'identification': '666', 'x': 0, 'y': 0,
         'is_busy': False},
    ]


def get_customers_data():
    return [
        {'identification': '1', 'x': 10, 'y': 10},
        {'identification': '2', 'x': 15, 'y': 20},
        {'identification': '3', 'x': 8, 'y': 19},
    ]


def get_services_data():
    return [
        {'date': '2021-08-19', 'requesting_client': '1'},
        {'date': '2021-08-19', 'requesting_client': '3'},
        {'date': '2021-08-20', 'requesting_client': '2'},
        {'date': '2021-08-20', 'requesting_client': '3'},
        {'date': '2021-08-20', 'requesting_client': '1'},
    ]


def get_gas_stations_data():
    return [
        {'name': 'Gasolineria 1', 'x': 5, 'y': 16},
        {'name': 'Gasolineria 2', 'x': 10, 'y': 16},
        {'name': 'Gasolineria 3', 'x': 3, 'y': 16},
        {'name': 'Gasolineria 4', 'x': 17, 'y': 16},
        {'name': 'Gasolineria 5', 'x': 20, 'y': 16},
    ]


def create_customer(data):
    location = Location.objects.create(
        pos_x=data.get('x'), pos_y=data.get('y'))
    Customer.objects.create(
        identification=data.get('identification'), location=location)


def create_driver(data):
    location = Location.objects.create(
        pos_x=data.get('x'), pos_y=data.get('y'))
    Driver.objects.create(
        name=data.get('name'), is_busy=data.get('is_busy'),
        identification=data.get('identification'), location=location)


def create_gas_station(data):
    location = Location.objects.create(
        pos_x=data.get('x'), pos_y=data.get('y'))
    gas_station = GasStation.objects.create(
        name=data.get('name'), location=location
    )
    gas_station.update_nearby_driver()


def create_service(data):
    date = make_aware(datetime.strptime(data.get('date'), '%Y-%m-%d'))
    requesting_client = Customer.objects.filter(
        identification=data.get('requesting_client')).first()
    gas_station = MapSimulator(requesting_client.location).\
        get_gas_station_nearby()
    service = Service.objects.create(
        requesting_client=requesting_client,
        responsible_driver=gas_station.nearby_driver,
        nearby_gas_station=gas_station,
        status=Service.DeliveryStatuses.DELIVERED, distance=0
    )
    service.date = date
    service.save()


def create_services():
    for service in get_services_data():
        create_service(service)


def create_customers():
    for customer in get_customers_data():
        create_customer(customer)


def create_drivers():
    for driver in get_drivers_data():
        create_driver(driver)


def create_gas_stations():
    for gas_station in get_gas_stations_data():
        create_gas_station(gas_station)