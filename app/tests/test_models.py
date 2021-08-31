from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import City, Location, Driver, Customer, GasStation, Service
from django.db.utils import IntegrityError


class CityModelTest(TestCase):
    def setUp(self):
        pass

    def test_city_complete_data(self):
        city = City.objects.create(name='Bogotá', width=100, height=100,
                                   velocity=2)
        self.assertIsNotNone(city, 'should create city')
    
    def test_no_negative_values(self):
        with self.assertRaises(ValidationError):
            city = City(name='City', width=-1, height=100, velocity=2)
            city.full_clean()
        with self.assertRaises(ValidationError):
            city = City(name='City', width=100, height=-1, velocity=2)
            city.full_clean()
            
    def test_city_str(self):
        city = City.objects.create(
            name='city name', width=100, height=100, velocity=1)
        self.assertEqual(str(city), 'city name', 'Should be city name')


class LocationModelTest(TestCase):
    def setUp(self):
        pass

    def test_location_complete_data(self):
        location = Location(pos_x=1, pos_y=1)
        self.assertIsNotNone(location, 'should create location')

    def test_location_no_negative_values(self):
        with self.assertRaises(ValidationError):
            location = Location(pos_x=-1, pos_y=1)
            location.full_clean()
        with self.assertRaises(ValidationError):
            location = Location(pos_x=1, pos_y=-1)
            location.full_clean()

    def test_location_distance(self):
        object_a = Location.objects.create(pos_x=20, pos_y=15)
        object_b = Location.objects.create(pos_x=10, pos_y=10)
        with self.assertRaises(Exception):
            object_a.calculate_distance(None)
        distance = object_a.calculate_distance(object_b)
        self.assertEqual(
            distance, 11.180,
            'should calculate distance between two points')

    def test_location_str(self):
        location = Location.objects.create(pos_x=20, pos_y=15)
        self.assertEqual(str(location), '(20, 15)')


class DriverModelTest(TestCase):
    def setUp(self):
        pass

    def test_driver_complete_data(self):
        driver = Driver.objects.create(
            name='Denis Conductor', identification='111', is_busy=False)
        self.assertIsNotNone(driver, 'should create a driver')

    def test_validate_relation_location(self):
        driver = Driver(name='Denis Conductor', identification='111',
                        is_busy=False)
        driver_location = Location.objects.create(pos_x=10, pos_y=30)
        driver.location = driver_location
        driver.save()
        self.assertIsNotNone(driver.id)

    def test_driver_str(self):
        driver = Driver.objects.create(
            name='Denis Conductor', identification='111', is_busy=False)
        self.assertEqual(
            str(driver), '111', 'Should be 111')


class CustomerModelTest(TestCase):
    def setUp(self):
        pass

    def test_customer_complete_data(self):
        customer = Customer.objects.create(identification='222')
        self.assertIsNotNone(customer.id)

    def test_relation_location(self):
        customer_location = Location.objects.create(pos_x=10, pos_y=30)
        customer = Customer(identification='333',
                            location=customer_location)
        customer.save()
        self.assertIsNotNone(customer.id)
    
    def test_customer_str(self):
        customer = Customer(identification='333')
        self.assertEqual(str(customer), '333', 'Should be 333')


class GasStationModelTest(TestCase):
    drivers_data = [
        {'name': 'Juan', 'identification': '111', 'x': 20, 'y': 10,
         'is_busy': False},
        {'name': 'Angie', 'identification': '222', 'x': 15, 'y': 20,
         'is_busy': False}
    ]

    def setUp(self):
        self.__create_drivers()

    def __create_drivers(self):
        for driver in self.drivers_data:
            self.__create_driver_from_data(driver)

    def __create_driver_from_data(self, data):
        location = Location.objects.create(
            pos_x=data.get('x'), pos_y=data.get('y'))
        Driver.objects.create(
            name=data.get('name'), is_busy=data.get('is_busy'),
            identification=data.get('identification'), location=location)

    def test_gas_station_complete_data(self):
        gas_station = GasStation.objects.create(
            name='Gasolinería 1', has_gasoline=True, nearby_driver_distance=0)
        self.assertIsNotNone(gas_station.id, 'should create a gas station')
        
    def test_location_relation(self):
        gas_station_location = Location.objects.create(pos_x=10, pos_y=30)
        gas_station = GasStation.objects.create(
            name='Gasolinería 1', has_gasoline=True, nearby_driver_distance=0,
            location=gas_station_location
        )
        self.assertIsNotNone(
            gas_station.id, 'should create a gas station with location')

    def test_driver_relation(self):
        driver = self.__create_driver()
        gas_station_location = Location.objects.create(pos_x=40, pos_y=40)
        gas_station = GasStation.objects.create(
            name='Gasolinería 2', has_gasoline=True, nearby_driver_distance=0,
            location=gas_station_location, nearby_driver=driver
        )
        self.assertIsNotNone(
            gas_station.id, 'should create a gas station with nearby driver')

    def __create_driver(self):
        driver_location = Location.objects.create(pos_x=10, pos_y=30)
        driver = Driver.objects.create(
            name='Denis Conductor', identification='111', is_busy=False,
            location=driver_location)
        return driver

    def test_gas_station_str(self):
        gas_station = GasStation.objects.create(
            name='Gasolinería 2', has_gasoline=True, nearby_driver_distance=0)
        self.assertEqual(
            str(gas_station), 'Gasolinería 2', 'Should be Gasolinería 2'
        )

    def test_gas_station_update_nearby_driver(self):
        location = Location.objects.create(pos_x=16, pos_y=19)
        gas_station = GasStation.objects.create(
            name='Gasolinería 2', has_gasoline=True, location=location)
        gas_station.update_nearby_driver()
        self.assertEqual(
            gas_station.nearby_driver.name, 'Angie', 'Should be angie driver')
        self.assertEqual(
            gas_station.nearby_driver_distance, 1.414, 'Should be 1.414')
        self.assertEquals(
            gas_station.calculate_wait_time(), 2, 'Should be 2'
        )

    def test_gas_station_there_are_no_nearby_driver(self):
        Driver.objects.filter().update(is_busy=True)
        location = Location.objects.create(pos_x=16, pos_y=19)
        gas_station = GasStation.objects.create(
            name='Gasolinería 2', has_gasoline=True, location=location)
        gas_station.update_nearby_driver()
        self.assertIsNone(
            gas_station.nearby_driver, 'Should not have a nearby_driver')




class ServiceModelTest(TestCase):
    def setUp(self):
        pass

    def test_service_complete_data(self):
        customer = self.__get_customer()
        driver = self.__get_driver()
        gas_station = self.__get_gas_station()
        distance = 0
        service = Service.objects.create(
            date=datetime.now(), requesting_client=customer,
            responsible_driver=driver, distance=distance,
            nearby_gas_station=gas_station)
        self.assertIsNotNone(service.id, 'should create a service')
        self.assertEqual(service.status, Service.DeliveryStatuses.NEW,
                         'status should be new by default')

    def __get_customer(self):
        location = Location.objects.create(pos_x=10, pos_y=11)
        customer = Customer.objects.create(
            identification='123', location=location)
        return customer

    def __get_driver(self):
        location = Location.objects.create(pos_x=10, pos_y=13)
        driver = Driver.objects.create(
            name='Denis conductor', identification='123', location=location)
        return driver

    def __get_gas_station(self):
        location = Location.objects.create(pos_x=10, pos_y=15)
        gas_station = GasStation.objects.create(
            name='Gasolinearia test', has_gasoline=True, location=location)
        return gas_station

    def test_service_str(self):
        customer = self.__get_customer()
        driver = self.__get_driver()
        gas_station = self.__get_gas_station()
        distance = 0
        service = Service.objects.create(
            date=datetime.now(), requesting_client=customer,
            responsible_driver=driver, distance=distance,
            nearby_gas_station=gas_station)
        self.assertEquals(
            str(service), 'Servicio: (Cliente 123) (Solicitado)',
            'Should be "Servicio: (Cliente 123) (Solicitado)"')

    def test_calculate_time(self):
        customer = self.__get_customer()
        driver = self.__get_driver()
        gas_station = self.__get_gas_station()
        gas_station.update_nearby_driver()
        distance = float(gas_station.nearby_driver_distance) + customer.\
            location.calculate_distance(gas_station.location)
        service = Service.objects.create(
            date=datetime.now(), requesting_client=customer,
            responsible_driver=driver, distance=distance,
            nearby_gas_station=gas_station)

        self.assertEqual(service.calculate_wait_time(), 6, 'Should be 6')


