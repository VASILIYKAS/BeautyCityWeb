from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from AppHome.models import Client


class Salon(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название салона')
    address = models.CharField(max_length=200, verbose_name='Адрес салона')
    image = models.ImageField(
        upload_to='salons/',
        null=True,
        blank=True,
        verbose_name='Фото салона',
    )

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):
    SERVICES = [
        ('hairdressing_services', 'Парикмахерские услуги'),
        ('nail_service', 'Ногтевой сервис'),
        ('makeup', 'Макияж')
    ]

    group_services = models.CharField(
        choices=SERVICES,
        max_length=100,
        verbose_name='Группа услуг',
    )
    name = models.CharField(max_length=100, verbose_name='Услуга')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name='Цена',
    )
    image = models.ImageField(
        upload_to='services/',
        null=True,
        blank=True,
        verbose_name='Фото салона',
    )
    update_service = models.DateField(
        auto_now=True, verbose_name='Последнее обновление')
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата создания услуги')

    class Meta:
        verbose_name = 'Услугу'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.name}'


class Master(models.Model):
    CHOICE_SPECIALIZATION = [
        ('stylist', 'стилист'),
        ('make-up', 'визажист'),
        ('manicurist', 'мастер маникюра'),
        ('barber', 'парикмахер'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    speciality = models.CharField(
        choices=CHOICE_SPECIALIZATION,
        max_length=20,
        verbose_name='Специальность',
    )
    experience_years = models.PositiveIntegerField(
        default=0, verbose_name='Стаж лет')
    experience_months = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(11)],
        verbose_name='Стаж месяцев',
    )
    image = models.ImageField(
        upload_to='masters_photos/',
        null=True,
        blank=True,
        verbose_name='Фото мастера',
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='masters',
        verbose_name='Салон',
    )
    services = models.ManyToManyField(
        Service,
        related_name='masters',
        verbose_name='Услуги'
    )

    class Meta:
        verbose_name = 'Мастера'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.get_speciality_display()})'


class Appointment(models.Model):
    TIME_SLOTS = [
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('12:00', '12:00'),
        ('12:30', '12:30'),
        ('15:00', '15:00'),
        ('16:30', '16:30'),
        ('17:00', '17:00'),
        ('18:30', '18:30'),
        ('19:00', '19:00'),
    ]
    PAYMENT_STATUS = [
        ('paid', 'оплачено'),
        ('not_paid', 'не оплачено')
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='client_appointments',
        verbose_name='Клиент'
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name='salon_appointments',
        verbose_name='Салон',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_appointments',
        verbose_name='Услуга'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='master',
        verbose_name='Мастер',
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name='Цена',
    )
    date = models.DateField(verbose_name='Дата приёма')
    reception_time = models.CharField(
        choices=TIME_SLOTS,
        max_length=5,
        verbose_name='Время приёма',
    )
    status = models.CharField(
        choices=PAYMENT_STATUS,
        default='not_paid',
        max_length=20,
        verbose_name='Оплата'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания заявки')

    @classmethod
    def get_slot_employment(cls, master, date, reception_time):
        return cls.objects.filter(
            master=master,
            date=date,
            reception_time=reception_time
        ).exists()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f'Запись №{self.id}'
