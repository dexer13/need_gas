from django.contrib import admin
from .models import City, Location, Driver, Customer, GasStation, Service
# Register your models here.


class CityAdmin(admin.ModelAdmin):
    fields = ('name', 'width', 'height', 'velocity')
    list_display = ('name', 'width', 'height', 'velocity')


class LocationAdmin(admin.ModelAdmin):
    fields = ('pos_x', 'pos_y')
    list_display = ('id', 'pos_x', 'pos_y')


class DriverAdmin(admin.ModelAdmin):
    fields = ('name', 'identification', 'is_busy', 'location')
    list_display = ('name', 'identification', 'is_busy', 'location')


class CustomerAdmin(admin.ModelAdmin):
    fields = ('name', 'identification', 'location')
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('name', 'identification', 'location')


class GasStationAdmin(admin.ModelAdmin):
    fields = ('name', 'has_gasoline', 'nearby_driver_distance', 'location',
              'nearby_driver')
    list_display = ('name', 'has_gasoline', 'nearby_driver_distance',
                    'location', 'nearby_driver')


class ServiceAdmin(admin.ModelAdmin):
    fields = ('requesting_client', 'responsible_driver',
              'nearby_gas_station', 'status', 'distance')
    readonly_fields = ('date',)
    list_display = ('id', 'date', 'requesting_client', 'responsible_driver',
                    'nearby_gas_station', 'status', 'distance')


admin.site.register(City, CityAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(GasStation, GasStationAdmin)
admin.site.register(Service, ServiceAdmin)

