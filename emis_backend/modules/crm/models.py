import json
from datetime import datetime
from isdayoff import DateType, ProdCalendar

import asyncio
from django.db import models
from django.utils.translation import gettext_lazy as _
import base64
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from modules.files_manager.models import Attachment
from common.request import current_request
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from common.request import current_request
from phone_field import PhoneField

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Только буквы и цифры')
onlynumber = RegexValidator(r'^[0-9]*$', 'Только цифры')


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split("/")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


def path_file(instance, filename):
    ext = str(filename).split('.')[-1]
    return f'files/{instance.pk}/{slugify(str(filename))}.{ext}'


class Ntd(models.Model):
    """
        Нормативно-техническая документация
    """
    objects = models.Manager()

    def __str__(self):
        pass

    class Meta:
        managed = True
        verbose_name = 'Нормативно-техническая документация'
        verbose_name_plural = 'Нормативно-техническая документация'


class Rd(models.Model):
    """
        Разрешенная документация
    """
    objects = models.Manager()

    def __str__(self):
        pass

    class Meta:
        # managed = True
        verbose_name = 'Разрешенная документация'
        verbose_name_plural = 'Разрешенная документация'


class Department(models.Model):
    name = models.CharField(_("Название отдела"), max_length=255)

    def __str__(self):
        return self.name


class Personnel(models.Model):
    """
        модель Персонал
    """
    WORK_STATUS = [
        ('Р', _('Работает')),
        ('М', _('Межвахта')),
        ('У', _('Уволен'))
    ]
    name = models.CharField(_("ФИО"), max_length=70)
    position = models.CharField(_("Должность"), max_length=50, blank=True, null=True)
    status = models.CharField(_("Статус"), max_length=50,
                              choices=WORK_STATUS, blank=True, null=True)
    phone = PhoneNumberField(_("Телефон"), blank=True, null=True)
    phone1 = PhoneNumberField(_("Доп. телефон 1"), blank=True, null=True)
    phone2 = PhoneNumberField(_("Доп. телефон 2"), blank=True, null=True)
    code = models.ForeignKey('Code', verbose_name='Код ОКЗ', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(_("Электронная почта"), max_length=254, blank=True, null=True)
    birthday = models.DateField(verbose_name=_("Дата рождения"), blank=True, null=True)
    files = models.ManyToManyField(Attachment, verbose_name=_("Файлы"), blank=True)
    description = models.TextField(_("Важная информация"), blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name='Отдел', on_delete=models.CASCADE, blank=True, null=True)
    entity = models.ForeignKey('Entity', verbose_name='Обьект', on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_entity(self):
        return self.entity

    class Meta:
        # managed = True
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'


class TypeControl(models.Model):
    row1 = models.CharField(max_length=150, verbose_name=_("Вид контроля"))
    row2 = models.CharField(max_length=150, verbose_name=_("Дата окончания"))
    row3 = models.CharField(max_length=150, verbose_name=_("Объекты контроля"))
    objects = models.Manager()

    class Meta:
        verbose_name = 'Вид контроля'
        verbose_name_plural = 'Вид контроля'

    @property
    def identity(self):
        return

    @identity.setter
    def identity(self, value):
        return


class Identity(models.Model):
    personnel = models.ForeignKey(Personnel, verbose_name=_("Сотрудник"), on_delete=models.CASCADE)
    number = models.CharField(max_length=100, verbose_name=_("Номер"))
    date_of_issue = models.DateField(verbose_name=_("Дата выдачи"))
    level = models.IntegerField(verbose_name=_("Уровень"), blank=True, null=True)
    control = models.ManyToManyField(TypeControl, verbose_name=_("Вид контроля"), blank=True, null=True)
    cert_center = models.CharField(max_length=1000, verbose_name=_("Аттестационный центр"), blank=True, null=True)
    _file = models.ForeignKey(Attachment, verbose_name=_("Загрузка удостоверения"),
                              on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Удостоверение'
        verbose_name_plural = 'Удостоверения'

    def __str__(self):
        return self.number

    @property
    def file(self):
        if self._file:
            return self._file.attachments.url
        return ''

    @property
    def file_name(self):
        if self._file:
            return self._file.name
        return ''

    @file.setter
    def file(self, value):
        ext = value.name.split('.')[-1]
        name = value.name.split(f'.{ext}')[0]
        attach = Attachment.objects.create(
            name=f'{name}',
            attachments=value
        )
        self._file = attach


class AdditionalIdentity(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Наименование"), blank=True, null=True)
    personnel = models.ForeignKey(Personnel, verbose_name=_("Сотрудник"), on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    date1 = models.DateField(_("Дата выдачи"), auto_now=False, auto_now_add=False, blank=True, null=True)
    date2 = models.DateField(_("Дата окончания"), auto_now=False, auto_now_add=False, blank=True, null=True)
    cert_center = models.CharField(max_length=1000, verbose_name=_("Аттестационный центр"), blank=True, null=True)
    _file = models.ForeignKey(Attachment, verbose_name=_("Загрузка удостоверения"),
                              on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Дополнительное удостоверение'
        verbose_name_plural = 'Дополнительные удостоверения'

    def __str__(self):
        return self.name

    @property
    def file(self):
        if self._file:
            return self._file.attachments.url
        return ''

    @property
    def file_name(self):
        if self._file:
            return self._file.name
        return ''

    @file.setter
    def file(self, value):
        ext = value.name.split('.')[-1]
        name = value.name.split(f'.{ext}')[0]
        attach = Attachment.objects.create(
            name=f'{name}',
            attachments=value
        )
        self._file = attach


class EquipmentType(models.Model):
    number = models.CharField(max_length=4, verbose_name='Номер типа')
    name = models.CharField(max_length=255, verbose_name='Наименование', blank=True, null=True)

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'


class EquipmentStatus(models.Model):
    attr = models.CharField(max_length=4, verbose_name='Атрибут')
    name = models.CharField(max_length=255, verbose_name='Название статуса')

    class Meta:
        verbose_name = 'Статус оборудования'
        verbose_name_plural = 'Статусы оборудования'


class Equipment(models.Model):
    """
        модель оборудование
    """
    TYPE = [
        ('1', _('ВИК')),
        ('2', _('ПВК')),
        ('3', _('РК')),
        ('4', _('УК')),
        ('5', _('МК')),
        ('6', _('ПВТ')),
        ('7', _('ЭК')),
        ('8', _('Вспомогательное')),
        ('9', _('Мера')),
        ('10', _('Образец')),
        ('11', _('Эталон')),
        ('12', _('Дозиметрия')),

    ]
    VERIFICATION_STATUS = [
        ('И', _('Исправны (используют в работе)')),
        ('К', _('Законсервированы (в работе не используют)')),
        ('Р', _('Подлежат ремонту')),
        ('С', _('Подлежат списанию')),
    ]

    type = models.CharField(_("Тип"), max_length=50, choices=TYPE, blank=True, null=True)
    name = models.CharField(_("Наименование"), max_length=150)
    factory_number = models.CharField(_("Заводской номер"), max_length=50, blank=True, null=True)
    inventory_number = models.CharField(_("Инвентарный номер"), max_length=50, blank=True, null=True)
    purpose = models.CharField(_("Назначение"), max_length=250, blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name='Отдел', on_delete=models.CASCADE, blank=True, null=True)
    year_of_manufacture = models.CharField(_("Год изготовления"), max_length=4, blank=True, null=True)
    manufacture = models.CharField(_("Изготовитель"), max_length=150, blank=True, null=True)
    owner = models.CharField(_("Владелец"), max_length=50, blank=True, null=True)
    place_of_verification = models.CharField(_("Место проведения поверки"), max_length=50, blank=True, null=True)
    date_of_verification = models.DateField(_("Дата поверки"), auto_now=False, auto_now_add=False, blank=True,
                                            null=True)
    validity = models.DateField(_("Дата окончания поверки"), auto_now=False, auto_now_add=False, blank=True, null=True)
    status = models.CharField(_("Статус"), max_length=50,
                              choices=VERIFICATION_STATUS, blank=True, null=True)
    files = models.ManyToManyField(Attachment, verbose_name=_("Файлы"), blank=True)
    description = models.TextField(_("Важная информация"), blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.name} {self.factory_number}'

    class Meta:
        # managed = True
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

    @property
    def type_name(self):
        return [i[1] for i in self.TYPE if i[0] == self.type][0]

    def get_choice_name(self):

        if self.TYPE:
            for stat in self.TYPE:
                if stat[0] == self.status:
                    return stat[1]
        if self.VERIFICATION_STATUS:
            for stat in self.VERIFICATION_STATUS:
                if stat[0] == self.status:
                    return stat[1]

    def get_choice_name_type(self):
        for stat in self.TYPE:
            if stat[0] == self.type:
                return stat[1]

    def get_choice_name_status(self):
        for stat in self.VERIFICATION_STATUS:
            if stat[0] == self.status:
                return stat[1]

    @property
    def entity(self) -> models.QuerySet:
        entity = Entity.objects.filter(equipment__pk=self.pk)
        return entity

    def copy(self):
        equipment = self
        entity_qs = equipment.entity
        equipment.pk = None
        equipment.save()
        if entity_qs:
            for entity in entity_qs:
                entity.equipment.add(equipment)



class Entity(models.Model):
    """
        модель объект
    """
    NTD = [
        ('1', _('НТД-1')),
        ('2', _('НТД-2')),
        ('3', _('НТД-3'))
    ]

    RD = [
        ('1', _('РД-1')),
        ('2', _('РД-2')),
        ('3', _('РД-3'))
    ]
    name = models.CharField(_("Наименование"), max_length=150)
    directorate = models.CharField(_("Дирекция"), max_length=150)
    contractor = models.CharField(_("Заказчик"), max_length=50, help_text="Введите название заказчика")
    director_lnk = models.CharField(_("руководитель ЛНК"), max_length=50, help_text="Введите название руководитель ЛНК",
                                    blank=True, null=True)
    address = models.CharField(_("Адрес"), max_length=350, blank=True, null=True)
    ntd = models.CharField(_("Нормативно-техническая документация"), max_length=50,
                           choices=NTD, default=1, blank=True, null=True)
    rd = models.CharField(_("Разрешенная документация"), max_length=50,
                          choices=RD, default=1, blank=True, null=True)
    equipment = models.ManyToManyField(Equipment, verbose_name=_("Оборудование"), blank=True)
    description = models.TextField(_("Важная информация"), blank=True, null=True)
    files = models.ManyToManyField(Attachment, verbose_name=_("Файлы"), blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_choice_name(self):
        if self.NTD:
            for stat in self.NTD:
                if stat[0] == self.ntd:
                    return stat[1]
        if self.RD:
            for stat in self.RD:
                if stat[0] == self.rd:
                    return stat[1]

    class Meta:
        # managed = True
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

# ToDo delete this
class Subdivision(models.Model):
    TYPE = [
        ('1', _('Руководитель подразделения ЛНК')),
        ('2', _('Состав подразделения ЛНК')),
        ('3', _('Персонал взаимодействия'))
    ]
    type = models.CharField(_("Подразделение"), max_length=50, choices=TYPE, default=2)
    entity = models.ForeignKey(Entity, verbose_name="Обьект", on_delete=models.CASCADE)
    personnel = models.ManyToManyField(Personnel, verbose_name="Сотрудник", blank=True)
    objects = models.Manager

    @property
    def type_name(self):
        return [i[1] for i in self.TYPE if i[0] == self.type][0]

    @property
    def name(self):
        return self.type_name

    def __str__(self):
        return f'{self.type}_{self.personnel}'

    class Meta:
        ordering = ['type']


class History(models.Model):
    TYPE = [
        ('1', _('Информирование')),
        ('2', _('Перемещение')),
        ('3', _('Ремонт')),
        ('4', _('Иное'))
    ]
    created_on = models.DateTimeField(auto_now_add=True)
    type = models.CharField(_("Вид операции"), max_length=50,
                            choices=TYPE, default=1, blank=True, null=True)
    equipment = models.ForeignKey(Equipment, verbose_name=_("Оборудование"),
                                  on_delete=models.CASCADE, blank=True, null=True)
    entity = models.ForeignKey(Entity, verbose_name=_("Объект"),
                               on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=1000)
    _file = models.ForeignKey(Attachment, verbose_name=_("Файл"),
                              on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'История перемещений'
        verbose_name_plural = 'История перемещений'

    def __str__(self):
        return f'({self.created_on.ctime()}) {self.type_name}: {self.equipment.name}'

    @property
    def type_name(self):
        return [i[1] for i in self.TYPE if i[0] == self.type][0]

    @property
    def user(self):
        from modules.profiles.models import CustomUser
        user = CustomUser.objects.filter(history__pk=self.pk).first()
        if user:
            return user
        return None

    @property
    def user_name(self):
        if self.user:
            return self.user.get_full_name()
        return None

    @property
    def users(self):
        from modules.profiles.models import CustomUser
        return CustomUser.objects.all()

    def save(self, *args, **kwargs):
        request = current_request()
        if 'parent_pk' in request.GET:
            pk = request.GET.get('parent_pk')
            obj = Equipment.objects.get(pk=pk)
            self.equipment = obj

        if request.FILES:
            for f in request.FILES.getlist('file'):
                self.file = f

        super(History, self).save(*args, **kwargs)
        from modules.profiles.models import CustomUser
        user = current_request().user

        if not CustomUser.objects.filter(history__pk=self.pk):
            user.history.add(self)

    @property
    def file(self):
        if self._file:
            return self._file.attachments.url
        return ''

    @property
    def file_name(self):
        if self._file:
            return self._file.name
        return ''

    @file.setter
    def file(self, value):
        ext = value.name.split('.')[-1]
        name = value.name.split(f'.{ext}')[0]
        attach = Attachment.objects.create(
            name=f'{name}',
            attachments=value
        )
        self._file = attach


class HistoryTabel(models.Model):
    number = models.IntegerField(_("№ п/п"), max_length=64)
    contract_number = models.CharField(_("Номер договора"), max_length=64, blank=True, null=True)
    personnel = models.ForeignKey(
        'Personnel', verbose_name=_('Ответственный'), on_delete=models.CASCADE, blank=True, null=True
    )
    code = models.CharField(_("Код ОКЗ"), max_length=64, blank=True, null=True)
    position = models.CharField(_("Должность"), max_length=50, blank=True, null=True)
    salary = models.CharField(_("Заработная плата"), max_length=64, blank=True, null=True)
    start_date = models.DateField(verbose_name=_("Начало работы"), blank=True, null=True)
    end_date = models.DateField(verbose_name=_("Окончание работы"), blank=True, null=True)
    report_card = models.ForeignKey(
        'ReportCard', verbose_name=_("Табель"), on_delete=models.CASCADE, blank=True, null=True
    )
    salary_work = models.CharField(_("Зар. плата за отработанные дни"), max_length=64, blank=True, null=True)
    payment = models.CharField(_("Оплата медицинского обследования, проезда"), max_length=64, blank=True, null=True)
    award = models.CharField(_("Премия"), max_length=64, blank=True, null=True)
    penalty = models.CharField(_("Штраф"), max_length=64, blank=True, null=True)
    accrued = models.CharField(_("Начислено"), max_length=64, blank=True, null=True)
    description = models.CharField(_("Примечание"), max_length=512, blank=True, null=True)
    work_day = models.IntegerField(_("Отработано дней"), max_length=10, default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Список табелей'
        verbose_name_plural = 'Списки табелей'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__start_date = self.start_date
        self.__end_date = self.end_date

    def save(self, *args, **kwargs):
        if self.pk is None or (self.__start_date != self.start_date or self.__end_date != self.end_date):
            self.work_day = self.get_work_day()

        super().save(*args, **kwargs)

    def get_work_day(self):
        data = {}
        count_working_day = 0
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def work_day():
            nonlocal data
            calendar = ProdCalendar(locale='ru')
            data = await calendar.range_date(self.start_date, self.end_date)

        if self.start_date and self.end_date:
            loop.run_until_complete(work_day())

            for day, day_type in data.items():
                if day_type == DateType.WORKING:
                    count_working_day += 1

        return count_working_day


class Status(models.Model):
    """
        Статус
    """
    name = models.CharField(_("Наименование"), max_length=64)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class ReportCard(models.Model):
    """
        модель Табель
    """
    card = models.CharField(_("Табель"), max_length=64)
    period = models.CharField(_("Период"), max_length=70, blank=True, null=True)
    entity = models.ForeignKey('Entity', verbose_name='Обьект', on_delete=models.CASCADE, blank=True, null=True)
    responsible = models.ForeignKey('Personnel', verbose_name='Ответственный', on_delete=models.CASCADE, blank=True,
                                    null=True, related_name='responsible')
    customer = models.ForeignKey('Personnel', verbose_name='Заказчик', on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='customer')
    status = models.ForeignKey('Status', verbose_name='Статус', on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(_("Комментарий"), max_length=512, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    files = models.ManyToManyField(Attachment, verbose_name=_("Файлы"), blank=True)
    is_edit_history_tabel = models.BooleanField(default=True)
    user = models.ForeignKey(to='profiles.CustomUser', verbose_name='Пользователь',
                             on_delete=models.CASCADE, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.card

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__user = self.user

    class Meta:
        # managed = True
        verbose_name = 'Табель'
        verbose_name_plural = 'Табеля'

    def save(self, *args, **kwargs):
        if not self.__user:
            from modules.profiles.models import CustomUser
            request = current_request()
            user_id = request.auth.payload.get('user_id')
            self.user = CustomUser.objects.get(id=user_id)

        super().save(*args, **kwargs)

    def copy(self):
        report_card = self
        history_tabel = list(self.historytabel_set.all())
        report_card.pk = None
        report_card.save()
        for item in history_tabel:
            item.pk = None
            item.report_card = report_card
            item.save()


class Code(models.Model):
    """
        Код ОКЗ
    """
    name = models.CharField(_("Код"), max_length=256)

    class Meta:
        verbose_name = 'Код ОКЗ'
        verbose_name_plural = 'Коды ОКЗ'