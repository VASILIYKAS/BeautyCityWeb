from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Фамилия',
    )
    phone = PhoneNumberField(
        unique=True,
        region='RU',
        verbose_name='Телефон',
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Клиента'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Feedback(models.Model):
    author = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author}'


class Consultation(models.Model):
    STATUS = [
        ('new', 'новая'),
        ('work', 'в работе'),
        ('completed', 'завершена')
    ]

    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = PhoneNumberField(
        unique=True,
        region='RU',
        verbose_name='Телефон',
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name='Вопрос')
    status = models.CharField(
        choices=STATUS,
        default='new',
        max_length=10,
        verbose_name='Статус заявки'
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки на консультацию'

    def __str__(self):
        return f'Заявка №{self.id}'
