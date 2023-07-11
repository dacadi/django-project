from django.conf.urls.static import static
from django.urls import path, re_path

from stoodclub import settings
from .views import *

urlpatterns = [
    # Стартовая страница
    path('', start, name='start'),

    # Архив
    path('archive', archive, name='archive'),
    re_path(r'^archive/((?P<yearStart>[0-9]{4})[-\w]+(?P<yearEnd>[0-9]{4}))', year_archive),

    # О нас
    path('about', about, name='about'),

    # Формы регистрации на мероприятия
    path('registration_part', registration_part, name='registration_part'),
    path('event/<int:event>-<int:year>', registrated_list_part, name='registrated_list_part'),

    # Формы регистрации и формы авторизации
    path('accounts/login', LoginFormView.as_view(), name='autorisation'),
    path('accounts/profile', profile, name='profile'),
    path('accounts/register', registration, name="registration"),
    path('accounts/enter', LogoutView.as_view(), name='logout'),

    # Отчестность
    path('guestsevent/<int:event>-<int:year>', guests, name='guests'),

    #Регистраци на мероприятие в качестве зрителя
    path('registration_guest', registration_guest, name='registration_guest'),
    path('archive_period', reg_period, name='archive_period'),
]
