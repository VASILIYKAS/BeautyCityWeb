from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('notes/', views.notes, name='notes'),
    path('popup/', views.popup, name='popup'),
    path('service/', views.service, name='service'),
    path('serviceFinally/', views.service_finally, name='service_finally'),
    path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


