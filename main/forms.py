from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms.fields import EmailField
from django.forms.forms import Form

User = get_user_model()



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин', min_length=5, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Проверка пароля', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', min_length=5, max_length=150)
    last_name = forms.CharField(label='Фамилия', min_length=5, max_length=150)


    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.password = self.cleaned_data["password"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user




class GuestsForm(ModelForm):
    class Meta:
        model = Guests
        fields = ['guest_name', 'guest_surname', 'guest_part', 'event', 'id_part_year']
        widgets = {
            'guest_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Имя"
            }),
            'guest_surname': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Фамилия"
            }),
            'guest_part': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Отчество"
            })
        }


class RegistrationForm(ModelForm):
    class Meta:
        model = Participants
        fields = ['team_name', 'event', 'id_part_year', 'id_resident']
        widgets = {
            'id_resident': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Ваш ID"
            }),
            'event': TextInput(attrs={
                'class': "form-control",
                'placeholder': "ID мероприятия"
            }),
            'id_part_year': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Год участия"
            }),
            'team_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Название команды"
            })}



# Форма создания записи в Базе данных



class NewPeriodForm(forms.Form):
    period = forms.CharField(max_length=8)
    year_start = forms.DecimalField(max_digits=4, decimal_places=0)
    year_end = forms.DecimalField(max_digits=4, decimal_places=0)
