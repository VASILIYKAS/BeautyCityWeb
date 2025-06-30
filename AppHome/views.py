import json

from django.contrib.auth import login
from django.shortcuts import render, redirect
from AppService.models import Salon, Service, Master
from AppHome.models import Feedback
from AppHome.forms import ClientRegistrationForm
from AppHome.forms import ConsultationRequestForm
from django.http import JsonResponse
from django.urls import reverse



def index(request):
    registration_form = ClientRegistrationForm()
    consultation_form = ConsultationRequestForm()

    consultation_success = False

    if request.method == 'POST':
        if 'email' in request.POST and 'password' in request.POST:
            registration_form = ClientRegistrationForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)
                return redirect('home')
        elif 'name' in request.POST and 'phone' in request.POST:
            consultation_form = ConsultationRequestForm(request.POST)
            if consultation_form.is_valid():
                consultation_form.save()
                consultation_success = True
                consultation_form = ConsultationRequestForm()

    salons = Salon.objects.all()
    services = Service.objects.all()
    masters = Master.objects.all()
    feedbacks = Feedback.objects.all()
    context = {
        'salons': salons,
        'services': services,
        'masters': masters,
        'feedbacks': feedbacks,
        'consultation_form': consultation_form,
        'consultation_success': consultation_success,
        'form': registration_form,
    }

    return render(request, 'index.html', context)


def notes(request):
    return render(request, 'notes.html')


def popup(request):
    return render(request, 'popup.html')


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


