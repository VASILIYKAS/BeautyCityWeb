from django.contrib import admin
from .models import Master, Salon


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'speciality',)
	list_filter = ('speciality',)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
	list_display = ('name', 'address')
