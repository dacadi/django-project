from django.db import models
from django.db.models import UniqueConstraint
from django.forms import ModelForm


class Event(models.Model):
    event = models.CharField(max_length=40, db_index=True, verbose_name='Мероприятие')
    content = models.TextField('Контент')
    photo = models.ImageField('Фото', upload_to="photos/events")
    is_Published = models.BooleanField('Опубликовано', default=True)

    def __str__(self):
        return self.event
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Archive(models.Model):
    period = models.CharField('Учебный год', max_length=8)
    year_start = models.DecimalField('С', max_digits=4, decimal_places=0)
    year_end = models.DecimalField('По', max_digits=4, decimal_places=0)
    url_photo = models.CharField('Адрес архива с фото', max_length=30)
    url_video = models.CharField('Адрес архива с видео', max_length=30)
    arch_photo = models.ImageField('Фото', upload_to="photos/arch/%Y")
    arch_video = models.ImageField('Фото видео', upload_to="photos/arch/%Y")

    def __str__(self):
        return self.period

    class Meta:
        verbose_name = 'Год'
        verbose_name_plural = 'Годы'


class Nominations(models.Model):
    event = models.ForeignKey('Event', on_delete=models.PROTECT, null=True)
    nomination = models.CharField('Номинация', max_length=60)

    def __str__(self):
        return self.nomination

    class Meta:
        verbose_name = 'Номинация'
        verbose_name_plural = 'Номинации'


class Participants(models.Model):
    team_name = models.CharField(max_length=40, null=True)
    event = models.ForeignKey('Event', on_delete=models.PROTECT)
    id_part_year = models.ForeignKey('Archive', on_delete=models.PROTECT)
    id_resident = models.ForeignKey('Residents', on_delete=models.PROTECT)

    def __str__(self):
        return self.id_resident

    class Meta:
        verbose_name = 'Участники'
        verbose_name_plural = 'Участник'
        constraints = [
            UniqueConstraint(fields=['id_resident', 'event', 'id_part_year'], name='unique_participation')
        ]


class Guests(models.Model):
    guest_name = models.CharField('Имя', max_length=40)
    guest_surname = models.CharField('Фамилия', max_length=40)
    guest_part = models.CharField('Отчество', max_length=40, null=True)
    event = models.ForeignKey('Event', default=1, on_delete=models.PROTECT)
    id_part_year = models.ForeignKey('Archive', default=20202021, on_delete=models.PROTECT)

    def __str__(self):
        return self.guest_name

    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'


class Winner(models.Model):
    id_par = models.ForeignKey('Residents', on_delete=models.PROTECT)
    event = models.ForeignKey('Event', on_delete=models.PROTECT)
    id_part_year = models.ForeignKey('Archive', on_delete=models.PROTECT)
    id_nomination = models.ForeignKey('Nominations', on_delete=models.PROTECT)

    def __str__(self):
        return self.id_par

    class Meta:
        verbose_name = 'Победитель'
        verbose_name_plural = 'Победители'


class News(models.Model):
    id_part_year = models.ForeignKey('Archive', on_delete=models.PROTECT)
    title = models.CharField('Заголовок', max_length=40)
    new = models.TextField('Содержание')
    photo_n = models.ImageField()
    url = models.CharField("Доп ссылка", max_length=40)
    for_guests = models.BooleanField("Доступ гостям",default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Residents(models.Model):
    id = models.IntegerField().primary_key=True
    resid_name = models.CharField('Имя', max_length=40)
    resid_surname = models.CharField('Фамилия', max_length=40)
    birth_date = models.DateTimeField("Дата рождения")
    login = models.CharField("Логин", max_length=40)
    password = models.CharField("Пароль", max_length=60)
    administrator = models.BooleanField("Администратор", default=False)


    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участник'


class Admins(models.Model):
    id_admin = models.DecimalField(max_digits=2, decimal_places=0).primary_key
    adm_code = models.DecimalField(max_digits=2, decimal_places=0).primary_key
    name_admin = models.CharField(max_length=40)
    surname_admin = models.CharField(max_length=40)
    post_admin = models.CharField(max_length=30).unique
    telephone_numb = models.DecimalField(max_digits=11, decimal_places=0)
    url_vk = models.CharField(max_length=30)
    admin_photo = models.ImageField(upload_to='photos/adm')

    def __str__(self):
        return (self.name_admin, self.surname_admin)

    class Meta:
        verbose_name = 'Администраторы'
        verbose_name_plural = 'Администратор'


class ArchiveForm(ModelForm):
    class Meta:
        model = Archive
        fields = ['period', 'year_start', 'year_end']
