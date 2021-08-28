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
        customer = Customer.objects.create(
            name='Denis Cliente', identification='222')
        self.assertIsNotNone(customer.id)

    def test_relation_location(self):
        customer_location = Location.objects.create(pos_x=10, pos_y=30)
        customer = Customer(name='Denis Cliente', identification='333',
                            location=customer_location)
        customer.save()
        self.assertIsNotNone(customer.id)
    
    def test_customer_str(self):
        customer = Customer(name='Denis Cliente', identification='333')
        self.assertEqual(str(customer), '333', 'Should be 333')


class GasStationModelTest(TestCase):
    def setUp(self):
        pass

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
        customer = Customer.objects.create(
            name='denis cliente', identification='123')
        return customer

    def __get_driver(self):
        driver = Driver.objects.create(
            name='Denis conductor', identification='123')
        return driver

    def __get_gas_station(self):
        gas_station = GasStation.objects.create(
            name='Gasolinearia test', has_gasoline=True)
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
