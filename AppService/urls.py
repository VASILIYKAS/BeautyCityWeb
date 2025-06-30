from django.urls import path

from . import views


urlpatterns = [
    path('service/', views.page_service, name='service'),
]
