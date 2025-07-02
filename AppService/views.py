from django.shortcuts import render, redirect
from datetime import datetime
from .models import Salon, Service, Master, Appointment
from AppHome.models import Client
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def get_groups_services():
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
    if request.method == 'POST':
        salon_id = request.POST.get('salon')
        salon = Salon.objects.get(id=salon_id)
        request.session['selected_salon_id'] = salon_id
        print(f"Выбран салон: {salon.name}, адрес: {salon.address}")
        return redirect('service_service')

    salons = Salon.objects.all()
    return render(request, 'service.html', {'salons': salons})


def fetch_service(request):
    if 'selected_salon_id' not in request.session:
        return redirect('service_salon')

    if request.method == 'POST':
        print("POST данные:", request.POST)  # Отладочный вывод
        service_id = request.POST.get('service')
        if service_id and service_id.isdigit():
            try:
                service = Service.objects.get(id=service_id)
                request.session['selected_service_id'] = service_id
                print(f"Выбрана услуга: {service.name}, price: {service.price}")
                return redirect('service_master')
            except Service.DoesNotExist:
                return render(request, 'service_service.html', {
                    'services': get_groups_services(),
                    'error': 'Выбранная услуга не найдена.'
                })
        else:
            print("Ошибка: service_id пустой или невалидный:", service_id)  # Отладочный вывод
            return render(request, 'service_service.html', {
                'services': get_groups_services(),
                'error': 'Пожалуйста, выберите услугу.'
            })

    return render(request, 'service_service.html', {
        'services': get_groups_services(),
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
            # Собираем полную дату и время
            datetime_str = f"{selected_date} {selected_time}"
            selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            # Сохраняем в сессии
            request.session['selected_datetime'] = datetime_str

            return redirect('confirm_service')

        except ValueError as e:
            return render(request, 'service_datetime.html', {
                'error': 'Неверный формат даты или времени'
            })

    return render(request, 'service_datetime.html')


def confirm_service(request):
    # Проверяем данные в сессии
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

    # Извлекаем данные из сессии
    salon_id = request.session['selected_salon_id']
    service_id = request.session['selected_service_id']
    master_id = request.session['selected_master_id']
    datetime_str = request.session['selected_datetime']

    selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    date = selected_datetime.date()
    time = selected_datetime.strftime('%H:%M')

    # Получаем объекты из базы данных
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
        # Данные формы
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        contactsTextarea = request.POST.get('contactsTextarea')

        # Проверка обязательных полей
        if not first_name or not phone:
            messages.error(request, 'Пожалуйста, заполните имя и номер телефона.')
            return redirect('confirm_service')

        # Получаем сессионные данные
        salon_id = request.session.get('selected_salon_id')
        service_id = request.session.get('selected_service_id')
        master_id = request.session.get('selected_master_id')
        datetime_str = request.session.get('selected_datetime')

        # Преобразование строки в дату и время
        selected_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        date = selected_datetime.date()
        time = selected_datetime.time().strftime('%H:%M')

        # Получаем объекты из базы данных
        salon = Salon.objects.get(id=int(salon_id))
        service = Service.objects.get(id=int(service_id))
        master = Master.objects.get(id=int(master_id))

        # Проверка занятости слота
        if Appointment.get_slot_employment(master, date, time):
            messages.error(request, 'Данный временной слот уже занят. Выберите другое время.')
            return redirect('confirm_service')

        # Создание клиента (либо берём существующего)
        client, created = Client.objects.get_or_create(first_name=first_name, phone=phone)

        # Цена услуги
        price = service.price

        # Создаём запись в БД
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

        # Чистка сессионных данных
        del request.session['selected_salon_id']
        del request.session['selected_service_id']
        del request.session['selected_master_id']
        del request.session['selected_datetime']

        # Сообщаем пользователю о успешном создании записи
        messages.success(request, 'Ваше бронирование успешно создано!')
        return redirect('home')

    return redirect('confirm_service')
