from django.contrib import admin
from .models import Master, Salon, Service, Appointment


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'speciality',)
	list_filter = ('speciality',)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
	list_display = ('name', 'address')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'group_services', 'update_service')
	list_filter = ('group_services', 'update_service',)
	readonly_fields = ('update_service', 'created_at',)
	

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ('id', 'client', 'master', 'date', 'reception_time')
	list_filter = ('master', 'date',)
	readonly_fields = ('created_at',)
