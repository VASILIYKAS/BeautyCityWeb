from django.contrib.auth import login
from django.shortcuts import render, redirect
from AppService.models import Salon, Service, Master
from AppHome.forms import ClientRegistrationForm


def index(request):
    salons = Salon.objects.all()
    services = Service.objects.all()
    masters = Master.objects.all()

    context = {
        'salons': salons,
        'services': services,
        'masters': masters,
    }

    return render(request, 'index.html', context)


def notes(request):
    return render(request, 'notes.html')


def popup(request):
    return render(request, 'popup.html')


def service(request):
    return render(request, 'service.html')


def service_finally(request):
    return render(request, 'serviceFinally.html')


def register(request):
	if request.method == 'POST':
		form = ClientRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
	else:
		form = ClientRegistrationForm()

	return render(request, 'registration/register.html', {'form': form})

def privacy_policy_view(request):
	return render(request, 'privacy_policy.html')

