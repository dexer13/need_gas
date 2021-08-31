from django.core.management.base import BaseCommand
from app.core import UpdateCustomer


class Command(BaseCommand):
    help = 'Actualizar la información de los clientes'

    def handle(self, *args, **kwargs):
        try:
            if UpdateCustomer().update_customer_from_service():
                print('Información actualizada')
            else:
                print('Error al actualizar la información')
        except Exception as e:
            print(e)
            print('Error al actualizar la información de los clientes')