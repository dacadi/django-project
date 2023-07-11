from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.template.defaulttags import url
from django.views.generic import TemplateView, FormView, View, CreateView
from django.contrib import auth

from .forms import *
from .models import *


def auth_user(req):
    menu = [{'title': "О нас", 'url_name': "about"},
            {'title': "Архив", 'url_name': "archive"},
            {'title': "Заявка гостя", 'url_name': "archive_period"}]
    if req.user.is_authenticated:
        menu.append({'title': "Заявка участника", 'url_name': "registration_part"})
        menu.append({'title': "Зарегистрировать год", 'url_name': "archive_period"})
        fn = auth.get_user(req).first_name
        un = auth.get_user(req)
        if req.user.is_superuser:
            menu.append({'title': "Отчестность", 'url_name': "registration_part"})
        return [fn, un, menu]
    else:
        return ['', 'there is no user', menu]

def start(request):
    [first_name, user, menu] = auth_user(request)
    start = {'menu': menu,
             'user': user,
             'first_name': first_name}
    return render(request, 'main/start.html', start)


def archive(request):
    year = Archive.objects.all()
    [first_name, user, menu] = auth_user(request)
    archive = {
        'title': 'Архив',
        'years': year,
        'menu': menu,
        'user': user,
        'first_name': first_name
    }
    return render(request, 'main/archive_test.html', archive)


def year_archive(request, yearStart, yearEnd):
    [first_name, user, menu] = auth_user(request)
    content = {
        'yearStart': yearStart,
        'yearEnd': yearEnd,
        'menu': menu,
        'user': user,
             'first_name': first_name
    }
    return render(request, 'main/year_arch_test.html', content)


def about(request):
    [first_name, user, menu] = auth_user(request)
    about = {
        'title': 'О нас',
        'menu': menu,
        'user': user,
        'first_name': first_name
    }
    return render(request, 'main/about.html', about)


def registration_guest(request):
    [first_name, user, menu] = auth_user(request)
    form = GuestsForm()
    error=''
    if request.method=="post":
        form = GuestsForm(request.POST)
        if form.is_valid():
            form.save()
            return(redirect('start'))
        else:
            error ='Форма заполнена неверно'

            return (redirect('start'))
    resident = {
            'title': 'Регистрация гостей',
            'user': user,
            'menu': menu,
             'first_name': first_name,
            'form': form,
            'error': error
            }
    return render(request, 'main/registration_guest.html', resident)



def registration_part(request):
    [first_name, user, menu] = auth_user(request)
    username = auth.get_user(request).username
    events = []
    i = 1
    for k in Event.objects.all():
        ev = {}
        ev['id'] = i
        ev['event'] = k
        events.append(ev)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            event = form.data['event']
            year = form.data['id_part_year']
            return redirect(f'event/{event}-{year}')
    form = RegistrationForm()
    resident = {
            'title': 'Регистрация участников',
            'form': form,
            'username': username,
            'menu': menu,
            'user': user,
            'first_name': first_name,
            'event': events
            }
    return render(request, 'main/registration_part.html', resident)


def registrated_list_part(request, event, year):
    [first_name, user, menu] = auth_user(request)
    event_n = Event.objects.get(id = event)
    part = Participants.objects.filter(id_part_year = year)
    dict = {'event': event_n,
            'part': part,
            'menu': menu,
            'user': user,
             'first_name': first_name}
    return render(request, 'main/registrated_list_part.html', dict)



class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "main/authorisation.html"
    success_url = "profile"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def profile(request):
    [first_name, user, menu] = auth_user(request)
    about = {
        'title': 'Профиль',
        'menu': menu,
        'user': user,
        'first_name': first_name
    }
    return render(request, 'main/profile.html', about)


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm()
        if form.is_valid():
            form.save()
            return(redirect('profile'))
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, "main/registration.html", context)



class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "profile"
    template_name = "main/registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


def pageNotFound(request, exception):
    return render(request, 'main/notFound.html')


def guests(request, event, year):
    [first_name, user, menu] = auth_user(request)
    event_n = Event.objects.get(id = event)
    guests = Guests.objects.filter(id_part_year = year)
    dict = {'event': event_n,
            'guests': guests,
            'menu': menu,
            'user': user,
             'first_name': first_name}
    return render(request, 'main/guests.html', dict)

# Представление добавления года регистрации
def reg_period(request):
    [first_name, user, menu] = auth_user(request)
    form = NewPeriodForm()
    error=''
    if request.method=="post":
        form = NewPeriodForm(request.POST)
        if form.is_valid():
            form.save()
            return(redirect('start'))
        else:
            form.save()
            return (redirect('start'))
    resident = {
            'title': 'Регистрация гостей',
            'user': user,
            'menu': menu,
             'first_name': first_name,
            'form': form,
            'error': error
            }
    return render(request, 'main/archive_period.html', resident)