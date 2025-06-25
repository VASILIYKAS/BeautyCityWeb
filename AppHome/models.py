from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
	first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Имя')
	last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Фамилия')
	phone = PhoneNumberField(unique=True, region='RU', verbose_name='Телефон')
	created_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

	class Meta:
		verbose_name = 'Клиента'
		verbose_name_plural = 'Клиенты'

	def __str__(self):
		return f'{self.first_name}'
