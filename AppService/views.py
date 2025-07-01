from django.shortcuts import render
from django.http import JsonResponse
import json

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


def receive_salon_name(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		salon_name = data.get('name')
		request.session['selected_salon'] = salon_name

		return JsonResponse({'status': 'ok'})

	return JsonResponse({'error': 'invalid request'}, status=400)


def page_service(request):
	salons = Salon.objects.all()
	selected_salon_name = request.session.get('selected_salon')
	masters = Master.objects.none()

	if selected_salon_name:
		selected_salon = Salon.objects.get(name=selected_salon_name)
		masters = Master.objects.filter(salon=selected_salon)

	context = {
		'salons': salons,
		'services': get_groups_services(),
		'masters': masters,
	}

	return render(request, 'service.html', {'context': context})
