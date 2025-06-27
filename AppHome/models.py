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
	created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

	class Meta:
		verbose_name = 'Клиента'
		verbose_name_plural = 'Клиенты'

	def __str__(self):
		return f'{self.first_name} {self.last_name}'
