from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import Client

class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=False, label='Имя')
    last_name = forms.CharField(max_length=100, required=False, label='Фамилия')
    phone = PhoneNumberField(region='RU', required=True, label='Телефон')

    class Meta(UserCreationForm.Meta):
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if Client.objects.filter(phone=phone).exists():
            raise ValidationError("Клиент с таким номером телефона уже зарегистрирован.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()


            client = Client.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone=self.cleaned_data['phone']
            )
        return user
