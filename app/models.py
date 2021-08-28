import math
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'Modelo base'


class City(BaseModel):
    name = models.TextField(max_length=30, verbose_name='Nombre')
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

    class Meta:
        db_table = 'driver'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'


class Customer(BaseModel):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    identification = models.CharField(
        max_length=15, verbose_name='Número de identificación')
    location = models.ForeignKey(
        Location, verbose_name='Ubicación del cliente', null=True,
        on_delete=models.PROTECT)

    class Meta:
        db_table = 'customer'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class GasStation(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    has_gasoline = models.BooleanField(
        default=True, verbose_name='Tiene gasolina')
    nearby_driver_distance = models.DecimalField(
        default=0, decimal_places=3, max_digits=10)
    location = models.ForeignKey(
        Location, verbose_name='Ubicación de la gasolinería', null=True,
        on_delete=models.PROTECT)
    nearby_driver = models.ForeignKey(
        Driver, on_delete=models.PROTECT, null=True,
        verbose_name='Conductor mas cercano')

    class Meta:
        db_table = 'gas_station'
        verbose_name = 'Gasolineria'
        verbose_name_plural = 'Gasolinerias'