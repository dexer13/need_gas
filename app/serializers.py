from .models import Service, Driver, GasStation, Customer
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['date', 'requesting_client', 'responsible_driver',
                  'nearby_gas_station', 'status', 'distance']


class DriverDistanceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField('get_distance')

    def __init__(self, *args, **kwargs):
        self.target_location = kwargs['context'].pop('target_location', None)
        super(DriverDistanceSerializer, self).__init__(*args, **kwargs)

    def get_distance(self, driver):
        return driver.location.calculate_distance(self.target_location)

    class Meta:
        model = Driver
        fields = ['name', 'identification', 'is_busy', 'location', 'distance']


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = '__all__'
        depth = 1


class GasStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasStation
        fields = '__all__'
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1