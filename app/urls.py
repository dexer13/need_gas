from django.urls import path
from .views import ServiceCustomerListView, ServiceDriverListView, \
    ServiceRequireServiceView, DriversByLocationListView, MapInfoView, \
    RequestServiceView


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
    path('info_map/', MapInfoView.as_view(), name='info_map'),
    path('request_service/<str:client_identification>/',
         RequestServiceView.as_view(), name='request_service'),
]
