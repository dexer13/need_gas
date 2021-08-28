from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import City, Location, Driver, Customer, GasStation
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

