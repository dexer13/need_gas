from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from ..admin import CityAdmin, LocationAdmin, DriverAdmin, CustomerAdmin, \
    GasStationAdmin, ServiceAdmin
from ..models import City, Location, Driver, Customer, GasStation, Service


class TestCityModelAdmin(TestCase):
    def setUp(self):
        pass

    def tests_exists_model_admin(self):
        city_model_admin = CityAdmin(model=City, admin_site=AdminSite())
        self.assertEqual(
            city_model_admin.model, City, 'should be same City model'
        )


class TestLocationModelAdmin(TestCase):
    def setUp(self):
        pass

    def test_exists_model_admin(self):
        location_model_admin = LocationAdmin(
            model=Location, admin_site=AdminSite)
        self.assertEqual(
            location_model_admin.model, Location, 'Should be location model'
        )


class TestDriverModelAdmin(TestCase):
    def setUp(self):
        pass

    def test_exists_model_admin(self):
        driver_model_admin = DriverAdmin(model=Driver, admin_site=AdminSite)
        self.assertEqual(
            driver_model_admin.model, Driver, 'Should be Driver model'
        )


class TestCustomerModelAdmin(TestCase):
    def setUp(self):
        pass

    def test_exists_model_admin(self):
        customer_model_admin = CustomerAdmin(
            model=Customer, admin_site=AdminSite)
        self.assertEqual(
            customer_model_admin.model, Customer, 'Should be Customer model'
        )


class TestGasStationModelAdmin(TestCase):
    def setUp(self):
        pass

    def test_exists_model_admin(self):
        gas_station_model_admin = GasStationAdmin(
            model=GasStation, admin_site=AdminSite)
        self.assertEqual(
            gas_station_model_admin.model, GasStation,
            'Should be GasStation Model'
        )


class TestServiceModelAdmin(TestCase):
    def setUp(self):
        pass

    def test_exists_model_admin(self):
        service_model_admin = ServiceAdmin(model=Service, admin_site=AdminSite)
        self.assertEqual(
            service_model_admin.model, Service, 'Should be Service model'
        )