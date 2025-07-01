from django.urls import path

from . import views


urlpatterns = [
    path('service/', views.page_service, name='service'),
    path('api/send-salon/', views.receive_salon_name, name='send_salon'),
]
