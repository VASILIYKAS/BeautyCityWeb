from django.contrib import admin
from .models import Master


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'speciality',)
	list_filter = ('speciality',)
