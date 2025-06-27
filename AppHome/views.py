from django.shortcuts import render
from AppService.models import Salon


def index(request):
	salons = Salon.objects.all()
	context = {'salons': salons}
	return render(request, 'index.html', context)


def notes(request):
	return render(request, 'notes.html')


def popup(request):
	return render(request, 'popup.html')


def service(request):
	return render(request, 'service.html')


def service_finally(request):
	return render(request, 'serviceFinally.html')