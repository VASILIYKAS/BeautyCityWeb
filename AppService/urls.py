from django.urls import path

from AppService.views import (
    fetch_salon,
    fetch_master,
    fetch_service,
    fetch_datetime,
    confirm_service,
    add_appointment,
    pick_master
)


urlpatterns = [
    path('service/', fetch_salon, name='service_salon'),
    path('service/service/', fetch_service, name='service_service'),
    path('service/master/', fetch_master, name='service_master'),
    path('service/datetime/', fetch_datetime, name='service_datetime'),
    path('service/confirm/', confirm_service, name='confirm_service'),
    path('service/add/', add_appointment, name='add_appointment'),
    path('book/master/<int:master_id>/', pick_master, name='pick_master'),
]
