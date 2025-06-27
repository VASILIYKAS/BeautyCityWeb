from django.contrib.auth import login
from django.shortcuts import render, redirect

from AppHome.forms import ClientRegistrationForm


def index(request):
	return render(request, 'index.html')


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