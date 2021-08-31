from django.core.management.base import BaseCommand
from app.models import GasStation

class Command(BaseCommand):
    help = 'Actualizar el conductor mas cercano a cada gasolinera'

    def handle(self, *args, **kwargs):
        try:
            gas_stations = GasStation.objects.all()
            for gas_station in gas_stations:
                gas_station.update_nearby_driver()
            print('Información actualizada')
        except Exception as e:
            print(e)
            print('Error al actualizar la gasolineras')