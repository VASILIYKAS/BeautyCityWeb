from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name', 'phone', 'created_at',)
	list_filter = ('created_at',)
	readonly_fields = ('created_at',)
