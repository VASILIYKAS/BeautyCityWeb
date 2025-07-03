from django.shortcuts import render, redirect
from datetime import datetime
from .models import Salon, Service, Master, Appointment
from AppHome.models import Client
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def get_groups_services(request):
    salon_id = request.session.get('selected_salon_id')

    if salon_id:
        services = Service.objects.filter(salons__id=salon_id)
    else:
        services = Service.objects.all()

    grouped_services = {}
    for service in services:
        group_name = service.get_group_services_display()
        if group_name not in grouped_services:
            grouped_services[group_name] = []

        grouped_services[group_name].append({
            'id': service.id,
            'name': service.name,
            'price': service.price
        })

    return grouped_services


def fetch_salon(request):
    keys_to_clear = [
        'selected_salon_id',
        'selected_service_id',
        'selected_master_id',
        'selected_master_name',
        'selected_salon_name'
    ]
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]

    if request.method == 'POST':
        salon_id = request.POST.get('salon')
        salon = Salon.objects.get(id=salon_id)
        request.session['selected_salon_id'] = salon_id
        print(f"Выбран салон: {salon.name}, адрес: {salon.address}")
        return redirect('service_service')

    salons = Salon.objects.all()
    return render(request, 'service.html', {'salons': salons})


def fetch_service(request):
    if 'selected_master_id' not in request.session and 'selected_salon_id' not in request.session:
        return redirect('service_salon')

    if request.method == 'POST':
        print("POST данные:", request.POST)
        service_id = request.POST.get('service')
        if service_id and service_id.isdigit():
            try:
                service = Service.objects.get(id=service_id)
                salon_id = request.session.get('selected_salon_id')
                if salon_id and not service.salons.filter(id=salon_id).exists():
                    return render(request, 'service_service.html', {
                        'services': get_groups_services(request),
                        'error': 'Эта услуга недоступна в выбранном салоне.'
                    })

                request.session['selected_service_id'] = service_id
                print(f"Выбрана услуга: {service.name}, price: {service.price}")

                if 'selected_master_id' in request.session:
                    master = Master.objects.get(id=request.session['selected_master_id'])
                    if not master.services.filter(id=service_id).exists():
                        del request.session['selected_master_id']
                        return redirect('service_master')
                    return redirect('service_datetime')
                else:
                    return redirect('service_master')

            except Service.DoesNotExist:
                return render(request, 'service_service.html', {
                    'services': get_groups_services(request),
                    'error': 'Выбранная услуга не найдена.'
                })
        else:
            print("Ошибка: service_id пустой или невалидный:", service_id)
            return render(request, 'service_service.html', {
                'services': get_groups_services(request),
                'error': 'Пожалуйста, выберите услугу.'
            })

    if 'selected_master_id' in request.session:
        master = Master.objects.get(id=request.session['selected_master_id'])
        salon_id = request.session.get('selected_salon_id')
        if salon_id:
            services = master.services.filter(salons__id=salon_id)
        else:
            services = master.services.all()
        return render(request, 'service_service.html', {
            'services': services,
            'master_selected': True
        })
    else:
        return render(request, 'service_service.html', {
            'services': get_groups_services(request),
        })


def fetch_master(request):
    if 'selected_salon_id' not in request.session:
        return redirect('service_salon')
    if 'selected_service_id' not in request.session:
        return redirect('service_service')

    if request.method == 'POST':
        master_id = request.POST.get('master')
        if master_id and master_id.isdigit():
            try:
                master = Master.objects.get(id=master_id)
                request.session['selected_master_id'] = master_id
                return redirect('service_datetime')
            except Master.DoesNotExist:
                return render(request, 'service_master.html', {
                    'masters': [],
                    'error': 'Выбранный мастер не найден.'
                })
        else:
            return render(request, 'service_master.html', {
                'masters': [],
                'error': 'Пожалуйста, выберите мастера.'
            })

    salon_id = request.session['selected_salon_id']
    service_id = request.session['selected_service_id']

    masters = Master.objects.filter(
        salon_id=salon_id,
        services__id=service_id
    ).distinct()

    if not masters.exists():
        if 'selected_master_id' in request.session:
            del request.session['selected_master_id']
        return render(request, 'service_master.html', {
            'masters': [],
            'error': 'Нет мастеров, предоставляющих выбранную услугу в этом салоне.'
        })

    return render(request, 'service_master.html', {
        'masters': masters,
    })


def fetch_datetime(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        selected_time = request.POST.get('selected_time')
        print('дата', selected_date)
        print('Время', selected_time)

        if not selected_date or not selected_time:
            return render(request, 'service_datetime.html', {
                'error': 'Пожалуйста, выберите дату и время'
            })

        try:
            datetime_str = f"{selected_date} {selected_time}"
            selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            request.session['selected_datetime'] = datetime_str

            return redirect('confirm_service')

        except ValueError as e:
            return render(request, 'service_datetime.html', {
                'error': 'Неверный формат даты или времени'
            })

    return render(request, 'service_datetime.html')


def pick_master(request, master_id):
    try:
        master = Master.objects.get(id=master_id)
        request.session['selected_master_id'] = master.id
        request.session['selected_master_name'] = f"{master.first_name} {master.last_name}"
        request.session['selected_salon_id'] = master.salon.id
        request.session['selected_salon_name'] = master.salon.name

        if 'selected_service_id' in request.session:
            del request.session['selected_service_id']
        return redirect('service_service')

    except Master.DoesNotExist:
        messages.error(request, 'Мастер не найден')
        return redirect('home')


def confirm_service(request):
    required_keys = [
        'selected_salon_id',
        'selected_service_id',
        'selected_master_id',
        'selected_datetime'
    ]

    if not all(key in request.session for key in required_keys):
        missing_keys = [key for key in required_keys if key not in request.session]
        print(f"Missing keys in session: {missing_keys}")
        return redirect('service_salon')

    salon_id = request.session['selected_salon_id']
    service_id = request.session['selected_service_id']
    master_id = request.session['selected_master_id']
    datetime_str = request.session['selected_datetime']

    selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    date = selected_datetime.date()
    time = selected_datetime.strftime('%H:%M')

    salon = Salon.objects.get(id=int(salon_id))
    service = Service.objects.get(id=int(service_id))
    master = Master.objects.get(id=int(master_id))

    return render(request, 'serviceFinally.html', {
        'salon': salon,
        'service': service,
        'master': master,
        'date': date,
        'time': time,
    })


def add_appointment(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        contactsTextarea = request.POST.get('contactsTextarea')

        if not first_name or not phone:
            messages.error(request, 'Пожалуйста, заполните имя и номер телефона.')
            return redirect('confirm_service')

        salon_id = request.session.get('selected_salon_id')
        service_id = request.session.get('selected_service_id')
        master_id = request.session.get('selected_master_id')
        datetime_str = request.session.get('selected_datetime')

        selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        date = selected_datetime.date()
        time = selected_datetime.time().strftime('%H:%M')

        salon = Salon.objects.get(id=int(salon_id))
        service = Service.objects.get(id=int(service_id))
        master = Master.objects.get(id=int(master_id))

        if Appointment.get_slot_employment(master, date, time):
            messages.error(request, 'Данный временной слот уже занят. Выберите другое время.')
            return redirect('confirm_service')

        client, created = Client.objects.get_or_create(first_name=first_name, phone=phone)

        price = service.price

        appointment = Appointment.objects.create(
            client=client,
            salon=salon,
            service=service,
            master=master,
            price=price,
            date=date,
            reception_time=time,
            status='not_paid',
        )

        del request.session['selected_salon_id']
        del request.session['selected_service_id']
        del request.session['selected_master_id']
        del request.session['selected_datetime']

        messages.success(request, 'Ваше бронирование успешно создано!')
        return redirect('home')

    return redirect('confirm_service')
