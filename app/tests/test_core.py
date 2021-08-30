from unittest.mock import patch
from django.test import TestCase

from .test_setups import get_drivers_data, get_gas_stations_data, \
    create_gas_station, create_driver
from ..core import UpdateCustomer, MapSimulator
from ..models import Customer, Driver, Location, GasStation


class MockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return [
            {
                "id": 1,
                "x": 52,
                "y": 24,
                "last-update": "2019-10-05 11:14:46"
            },
            {
                "id": 2,
                "x": 56,
                "y": 19,
                "last-update": "2020-07-28 02:08:45"
            },
        ]


class TestCoreUpdateCustomer(TestCase):
    def setUp(self):
        pass

    @patch("requests.get", return_value=MockResponse())
    def test_endpoint_customer(self, mocked):
        UpdateCustomer().update_customer_from_service()
        amount_customer = Customer.objects.all().count()
        self.assertEqual(amount_customer, 2, 'Should be two customer')


class TestMapSimulator(TestCase):

    def setUp(self):
        self.drivers_data = get_drivers_data()
        self.gas_stations_data = get_gas_stations_data()
        self.__create_drivers()
        self.__create_gas_stations()

    def __create_gas_stations(self):
        for gas_station in self.gas_stations_data:
            create_gas_station(gas_station)

    def __create_drivers(self):
        for driver in self.drivers_data:
            create_driver(driver)

    def test_get_drivers(self):
        drivers = MapSimulator(Location(pos_x=1, pos_y=1)).get_drivers()
        nearby_driver = drivers[0]
        self.assertEqual(
            nearby_driver.name, 'Andrea', 'Should be Andrea driver'
        )

    def test_get_drivers_no_busy(self):
        drivers = MapSimulator(Location(pos_x=13, pos_y=14)).\
            get_drivers_no_busy()
        nearby_driver = drivers[0]
        self.assertEqual(
            nearby_driver.name, 'Camilo', 'Should be Camilo driver'
        )

    def test_get_drivers_busy(self):
        drivers = MapSimulator(Location(pos_x=20, pos_y=11)). \
            get_drivers_busy()
        nearby_driver = drivers[0]
        self.assertEqual(
            nearby_driver.name, 'Juan', 'Should be Juan driver'
        )

    def test_get_nearby_driver(self):
        nearby_driver = MapSimulator(Location(pos_x=14, pos_y=19)).\
            get_nearby_driver()
        self.assertEqual(nearby_driver.name, 'Angie', 'Should be Angie driver')

    def test_gas_station_nearby(self):
        gas_station = MapSimulator(Location(pos_x=5, pos_y=20)).\
            get_gas_station_nearby()
        self.assertEqual(
            gas_station.name, 'Gasolineria 2', 'Should be Gasolineria 2')
