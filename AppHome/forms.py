from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from .models import Client
from AppService.models import ConsultationRequest


class ClientRegistrationForm(forms.Form):
    email = forms.EmailField(label='Адрес электронной почты', max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=False, label='Имя')
    last_name = forms.CharField(max_length=100, required=False, label='Фамилия')
    phone = PhoneNumberField(region='RU', required=True, label='Телефон')


    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput,
                                help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.')


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким адресом электронной почты уже зарегистрирован.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Client.objects.filter(phone=phone).exists():
            raise ValidationError("Клиент с таким номером телефона уже зарегистрирован.")
        return phone

    def save(self, commit=True):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        email = self.cleaned_data['email']
        username_value = email

        user = User(
            username=username_value,
            email=email,
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', '')
        )
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            client = Client.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone=self.cleaned_data['phone']
            )
        return user

class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['name', 'phone', 'question']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7(999)999-99-99', 'required': 'required'}),
            'question': forms.Textarea(attrs={'placeholder': 'Вопрос (необязательно)'}),
        }
        labels = {
            'name': '',
            'phone': '',
            'question': '',
        }
