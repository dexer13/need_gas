from datetime import datetime

from rest_framework import generics, status, views
from rest_framework.response import Response

from need_gas.PARAMETERS import VELOCITY
from .core import MapSimulator
from .models import Service, Driver, Location
from .serializers import ServiceSerializer, DriverDistanceSerializer


# Create your views here.


class ServiceCustomerListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        try:
            date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
            return Service.objects.filter(
                date__year=date.year,
                date__month=date.month,
                date__day=date.day,
            )
        except ValueError as e:
            return None

    def get(self, request, date):
        try:
            datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
            return super(ServiceCustomerListView, self).get(request)
        except ValueError as e:
            return Response(
                'El formato de la fecha debe ser YYY-MM-DD',
                status.HTTP_400_BAD_REQUEST
            )


class ServiceDriverListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        try:
            date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
            driver_identification = self.kwargs['identification']
            return Service.objects.filter(
                date__year=date.year,
                date__month=date.month,
                date__day=date.day,
                responsible_driver__identification=driver_identification
            )
        except ValueError as e:
            return None

    def get(self, request, identification, date):
        try:
            datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
            if not Driver.objects.filter(
                    identification=identification).exists():
                return Response(
                    f'No existe conductor con el numero de identificacíón '
                    f'{identification}',
                    status.HTTP_400_BAD_REQUEST
                )
            return super(ServiceDriverListView, self).get(request)
        except ValueError as e:
            return Response(
                'El formato de la fecha debe ser YYY-MM-DD',
                status.HTTP_400_BAD_REQUEST
            )


class ServiceRequireServiceView(views.APIView):

    def get(self, requests, x, y):
        from app.core import Util
        current_location = Location(pos_x=x, pos_y=y)
        gas_station = MapSimulator(current_location).\
            get_gas_station_nearby()
        time_wait_from_gas_station = Util.calculate_time_between_two_point(
            gas_station.location, Location(pos_x=x, pos_y=y)) * VELOCITY
        total_wait_time = time_wait_from_gas_station + gas_station.\
            calculate_wait_time()
        return Response(
            {'responsible_driver': gas_station.nearby_driver.identification,
             'wait_time': total_wait_time},
            status=status.HTTP_200_OK
        )


class DriversByLocationListView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverDistanceSerializer

    def get_queryset(self):
        location = Location(pos_x=self.kwargs['x'], pos_y=self.kwargs['y'])
        drivers = MapSimulator(location).get_drivers()
        return drivers

    def get_serializer_context(self):
        context = super(DriversByLocationListView, self).\
            get_serializer_context()
        context.update({'target_location': Location(
            pos_x=self.kwargs['x'], pos_y=self.kwargs['y'])}
        )
        return context

