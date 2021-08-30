from django.urls import path
from .views import ServiceCustomerListView, ServiceDriverListView, \
    ServiceRequireServiceView, DriversByLocationListView


urlpatterns = [
    path('services_by_customer/<str:date>/', ServiceCustomerListView.as_view(),
         name='services_by_date'),
    path('services_by_driver/<str:identification>/<str:date>/',
         ServiceDriverListView.as_view(),
         name='services_by_driver_and_date'),
    path('require_a_service/<int:x>/<int:y>/',
         ServiceRequireServiceView.as_view(),
         name='require_a_service'),
    path('drivers_sorted_by_distance/<int:x>/<int:y>/',
         DriversByLocationListView.as_view(),
         name='drivers_sorted_by_distance'),
]
