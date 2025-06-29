from django.shortcuts import render

from .models import Salon, Service, Master


def get_groups_services():
	services = Service.objects.all()
	grouped_services = {}

	for service in services:
		group_name = service.get_group_services_display()
		if group_name not in grouped_services:
			grouped_services[group_name] = []

		grouped_services[group_name].append({
			'name': service.name,
			'price': service.price
		})

	return grouped_services


def page_service(request):
	salons = Salon.objects.all()

	context = {
		'salons': salons,
		'services': get_groups_services()
	}

	return render(request, 'service.html', {'context': context})
