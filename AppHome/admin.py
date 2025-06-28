from django.contrib import admin
from .models import Client, Feedback, Consultation


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name', 'phone', 'created_at',)
	list_filter = ('created_at',)
	readonly_fields = ('created_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('author', 'created_at',)
	list_filter = ('created_at',)
	readonly_fields = ('created_at',)


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'phone', 'status', 'created_at',)
	list_filter = ('created_at', 'status')
	readonly_fields = ('created_at',)
