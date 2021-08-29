import math
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from need_gas.PARAMETERS import VELOCITY


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'Modelo base'


class City(BaseModel):
    name = models.CharField(max_length=30, verbose_name='Nombre')
    width = models.IntegerField(verbose_name='Ancho')
    height = models.IntegerField(verbose_name='Alto')
    velocity = models.IntegerField(verbose_name='Velocidad')

    def clean(self):
        self.__clean_width()
        self.__clean_height()

    def __clean_width(self):
        if self.width <= 0:
            raise ValidationError({
                'width': 'El valor del ancho debe ser mayor a cero'
            })

    def __clean_height(self):
        if self.height <= 0:
            raise ValidationError({
                'width': 'El valor del alto debe ser mayor a cero'
            })

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        db_table = 'city'


class Location(models.Model):
    pos_x = models.IntegerField(default=0, verbose_name='Posición X')
    pos_y = models.IntegerField(default=0, verbose_name='Posición Y')

    def clean(self):
        self.__clean_pos_x()
        self.__clean_pos_y()

    def __clean_pos_x(self):
        if self.pos_x < 0:
            raise ValidationError({
                'pos_x': 'El valor de la posición X debe ser mayor a cero'
            })

    def __clean_pos_y(self):
        if self.pos_y < 0:
            raise ValidationError({
                'pos_y': 'El valor de la posición Y debe ser mayor a cero'
            })

    def calculate_distance(self, target):
        if target is None:
            raise Exception('El objeto no puede ser None')
        distance = math.sqrt(
            math.pow(self.pos_x - target.pos_x, 2) +
            math.pow(self.pos_y - target.pos_y, 2)
        )
        return round(distance, 3)

    def __str__(self):
        return f'({self.pos_x}, {self.pos_y})'

    class Meta:
        db_table = 'location'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'


class Driver(BaseModel):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    identification = models.CharField(
        max_length=15, verbose_name='Número de identificación')
    is_busy = models.BooleanField(default=False)
    location = models.ForeignKey(
        Location, verbose_name='Ubicación del conductor', null=True,
        on_delete=models.PROTECT)

    def __str__(self):
        return self.identification

    class Meta:
        db_table = 'driver'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'


class Customer(BaseModel):
    identification = models.CharField(
        max_length=15, verbose_name='Número de identificación')
    location = models.ForeignKey(
        Location, verbose_name='Ubicación del cliente', null=True,
        on_delete=models.PROTECT)

    def __str__(self):
        return self.identification

    class Meta:
        db_table = 'customer'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class GasStation(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    has_gasoline = models.BooleanField(
        default=True, verbose_name='Tiene gasolina')
    nearby_driver_distance = models.DecimalField(
        decimal_places=3, max_digits=10, null=True)
    location = models.ForeignKey(
        Location, verbose_name='Ubicación de la gasolinería', null=True,
        on_delete=models.PROTECT)
    nearby_driver = models.ForeignKey(
        Driver, on_delete=models.PROTECT, null=True,
        verbose_name='Conductor mas cercano')

    def update_nearby_driver(self):
        from .core import MapSimulator
        nearby_driver = MapSimulator(self.location).get_nearby_driver()
        driver_distance = self.location.calculate_distance(
            nearby_driver.location)
        self.nearby_driver = nearby_driver
        self.nearby_driver_distance = driver_distance
        self.save()

    def calculate_wait_time(self):
        time_street = abs(self.location.pos_x - self.nearby_driver.location.
                          pos_x)
        time_avenues = abs(self.location.pos_y - self.nearby_driver.location.
                           pos_y)
        return (time_street + time_avenues) * VELOCITY


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gas_station'
        verbose_name = 'Gasolineria'
        verbose_name_plural = 'Gasolinerias'


class Service(BaseModel):
    class DeliveryStatuses(models.TextChoices):
        NEW = 'new', 'Solicitado'
        PICK_UP = 'pick_up', 'Recogiendo Gasolina'
        ON_DELIVERY = 'on_delivery', 'Enviando'
        DELIVERED = 'delivered', 'Entregado'
        ABORTED = 'aborted', 'Cancelado'
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    requesting_client = models.ForeignKey(
        Customer, on_delete=models.PROTECT,
        verbose_name='Cliente que solicita el servicio.')
    responsible_driver = models.ForeignKey(
        Driver, on_delete=models.PROTECT, verbose_name='Conductor responsable')
    nearby_gas_station = models.ForeignKey(
        GasStation, on_delete=models.PROTECT,
        verbose_name='Gasolinearia mas cercana')
    status = models.CharField(
        max_length=20, choices=DeliveryStatuses.choices,
        default=DeliveryStatuses.NEW, verbose_name='Estado del pedido')
    distance = models.IntegerField(verbose_name='Distancia')

    def calculate_wait_time(self):
        time_street = abs(self.requesting_client.location.pos_x -
                          self.nearby_gas_station.location.pos_x)
        time_avenues = abs(self.requesting_client.location.pos_y -
                           self.nearby_gas_station.location.pos_y)
        return (time_street + time_avenues +
                self.nearby_gas_station.calculate_wait_time()) * VELOCITY

    def __str__(self):
        return f'Servicio: (Cliente {self.requesting_client}) ' \
               f'({self.get_status_display()})'

    class Meta:
        ordering = ('-date',)
        db_table = 'service'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
