from rest_framework.test import APITestCase
from django.urls import reverse

from .test_setups import create_customers, create_drivers, \
    create_gas_stations, create_services


class ServicesViewTest(APITestCase):
    def setUp(self):
        create_customers()
        create_drivers()
        create_gas_stations()
        create_services()
        self.services_by_date_url = reverse(
            'services_by_date', args=['2021-08-19'])
        self.services_by_driver_and_date_url = reverse(
            'services_by_driver_and_date', args=['222', '2021-08-20'])
        self.require_a_service_url = reverse(
            'require_a_service', args=[10, 12])
        self.drivers_sorted_by_distance_url = reverse(
            'drivers_sorted_by_distance', args=[20, 15])

    def test_services_by_date(self):
        response = self.client.get(self.services_by_date_url)
        self.assertEqual(response.status_code, 200, 'Should be OK status')
        self.assertEquals(
            len(response.json()), 2, 'Should be 2 services for this day')

    def test_services_by_date_wrong_date(self):
        service_wrong_date = reverse('services_by_date', args=['19-08-2021'])
        response = self.client.get(service_wrong_date)
        self.assertEqual(
            response.status_code, 400, 'Should be BAD_REQUEST status')

    def test_service_by_driver_and_date(self):
        response = self.client.get(self.services_by_driver_and_date_url)
        self.assertEqual(response.status_code, 200, 'Should be OK status')
        self.assertEquals(len(response.json()), 1, 'Should be 1 driver')

    def test_service_by_driver_and_date_wrong_driver(self):
        service_wrong_date = reverse(
            'services_by_driver_and_date', args=['111', '19-08-2021'])
        response = self.client.get(service_wrong_date)
        self.assertEquals(response.status_code, 400, 'Should be bad request')
        self.assertEqual(
            response.json(), 'El formato de la fecha debe ser YYY-MM-DD',
            'Should return "El formato de la fecha debe ser YYY-MM-DD"'
        )

    def test_service_by_driver_and_date_wrong_date(self):
        service_wrong_driver = reverse(
            'services_by_driver_and_date', args=['000', '2021-08-20'])
        response = self.client.get(service_wrong_driver)
        self.assertEquals(response.status_code, 400, 'Should be bad request')
        self.assertEqual(
            response.json(),
            'No existe conductor con el numero de identificacíón 000',
            'Should return "No existe conductor con el numero de '
            'identificacíón 000"'
        )

    def test_require_a_service(self):
        response = self.client.get(self.require_a_service_url)
        self.assertEqual(response.status_code, 200, 'Should be OK status')
        self.assertEqual(
            response.json().get('responsible_driver'), '333',
            'should be driver identification 333')
        self.assertEqual(
            response.json().get('wait_time'), 8,
            'should be driver identification 8')

    def test_drivers_sorted_by_distance(self):
        response = self.client.get(self.drivers_sorted_by_distance_url)
        self.assertEqual(response.status_code, 200, 'Should be OK status')
        self.assertEqual(
            response.json()[0].get('identification'), '555',
            'Should be a driver with 555 identification')

