import requests
from .models import Customer, Location, Driver, GasStation


class UpdateCustomer:
    endpoint = 'https://gist.githubusercontent.com/CesarF/41958f4bc34240b7' \
               '5a83fce876836044/raw/b524588cb979fc6e3ec5a8913ee497d64509e' \
               '888/points.json'

    def update_customer_from_service(self):
        try:
            response = requests.get(self.endpoint)
            data = response.json()
            for json_data in data:
                self.json_to_customer(json_data)
            return True
        except Exception as e:
            raise Exception('Error al actualizar los datos')

    def json_to_customer(self, json_data):
        if self.__exists_customer(json_data.get('id')):
            self.__update_customer(json_data)
        self.__create_customer(json_data)

    def __exists_customer(self, pk_value):
        return Customer.objects.filter(id=pk_value).exists()

    def __update_customer(self, json_data):
        customer = Customer.objects.get_one(pk=json_data.get('id'))
        customer.identification = json_data.id
        customer.location.pos_x = json_data.get('x')
        customer.location.pos_y = json_data.get('y')
        customer.save()

    def __create_customer(self, json_data):
        location = Location.objects.create(
            pos_x=json_data.get('x'),
            pos_y=json_data.get('y')
        )
        Customer.objects.create(
            pk=json_data.get('id'),
            identification=json_data.get('id'),
            location=location
        )


class MapSimulator:

    def __init__(self, target):
        self.target = target

    def get_drivers(self):
        drivers = list(Driver.objects.all())
        return self.__sorted_objects_by_distance(drivers)
    
    def get_drivers_no_busy(self):
        drivers = list(Driver.objects.filter(is_busy=False))
        return self.__sorted_objects_by_distance(drivers)

    def get_drivers_busy(self):
        drivers = list(Driver.objects.filter(is_busy=True))
        return self.__sorted_objects_by_distance(drivers)

    def get_nearby_driver(self):
        return self.get_drivers_no_busy()[0]

    def get_gas_station_nearby(self):
        gas_stations = list(GasStation.objects.filter(has_gasoline=True).all())
        gas_stations = sorted(
            gas_stations,
            key=lambda o: o.location.calculate_distance(self.target) +
                          float(o.nearby_driver_distance))
        return gas_stations[0]

    def __sorted_objects_by_distance(self, objects):
        objects_sorted = sorted(
            objects, key=lambda o: o.location.calculate_distance(self.target))
        return objects_sorted


class Util:

    @staticmethod
    def calculate_time_between_two_point(point_a, point_b):
        time_x = abs(point_a.pos_x - point_b.pos_x)
        time_y = abs(point_a.pos_y - point_b.pos_y)
        return time_x + time_y

