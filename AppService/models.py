from django.core.validators import MaxValueValidator
from django.db import models


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
	experience_years = models.PositiveIntegerField(default=0, verbose_name='Стаж лет')
	experience_monts = models.PositiveIntegerField(
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

	class Meta:
		verbose_name = 'Мастера'
		verbose_name_plural = 'Мастера'

	def __str__(self):
		return f'{self.first_name} {self.last_name} ({self.get_speciality_display()})'


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
