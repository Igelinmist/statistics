from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from catalog.models import Unit


STANDARD_STATE_DATA = ('date', 'work',
                       'ostanov_cnt', 'pusk_cnt')
EXT_STATE_DATA = ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd')


def default_stat():
    return "wd=00:00,psk=0,ost=0"


def stat_timedelta(time_delta):
    sec = time_delta.total_seconds()
    hours, remainder = divmod(sec, 3600)
    minutes, sec = divmod(remainder, 60)
    return '%d:%02d' % (int(hours), int(minutes))


class Journal(models.Model):
    """
    Модель Журнала записей статистики
    по конкретному оборудованию
    """

    equipment = models.OneToOneField(Unit, on_delete=models.CASCADE)
    extended_stat = models.BooleanField(default=False)
    stat_by_parent = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    last_stat = models.CharField(max_length=250,
                                 default=default_stat,
                                 editable=False)

    class Meta:
        ordering = ['equipment__name']
        permissions = (
            ('view_journal_details', 'Может просматривать записи журнала'),
            ('view_journal_list', 'Может посмотреть список журналов'),
            ('create_journal_record', 'Может создать запись в журнале'),
            ('edit_journal_record', 'Может редактировать запись в журнале'),
            ('delete_journal_record', 'Может удалить запись в журнале'),
            ('create_journal_event', 'Может создать событие в журнале'),
            ('delete_journal_evtent', 'Может удалить событие в журнале'),
        )
        default_permissions = []
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'

    def __str__(self):
        plant_name = self.equipment.plant.name if self.equipment.plant else '-'
        return plant_name + ' \ ' + self.equipment.name

    def get_record_data(record_id=None):
        '''
        Description: Функция получения данных для инициализации полей формы
        существующей записью, включая расширенные состояния при наличии
        '''
        data = {}
        if record_id:
            rec = Record.objects.get(pk=record_id)
            for name in STANDARD_STATE_DATA:
                data[name] = rec.__getattribute__(name)
            if rec.journal.extended_stat:
                for state in EXT_STATE_DATA:
                    data[state] = timedelta(seconds=0)
                for state_item in rec.stateitem_set.all():
                    data[state_item.state.lower()] = state_item.time_in_state
            return data
        else:
            return None

    def get_state_summary(self, date_from=None):
        '''
        Description: Метод подсчета базовой статистики, возможно,
        от определенной даты
        '''
        if self.record_set.count():
            recs = self.record_set
            if date_from:
                recs = recs.filter(date__gte=date_from)
            stat = "wd=%s,psk=%d,ost=%d" % (
                stat_timedelta(recs.aggregate(models.Sum('work'))['work__sum']),
                recs.aggregate(models.Sum('pusk_cnt'))['pusk_cnt__sum'],
                recs.aggregate(models.Sum('ostanov_cnt'))['ostanov_cnt__sum'],)
        else:
            stat = "wd=00:00,psk=0,ost=0"
        return stat

    def update_state_cache(self):
        self.last_stat = self.get_state_summary()
        self.save()
        # обновление статистики для зависимых компонентов
        for unit in self.equipment.unit_set.all():
            if unit.journal and unit.journal.stat_by_parent:
                try:
                    date_from = unit.journal.eventitem_set.filter(
                        event='ZMN').order_by('-date')[0].date
                except IndexError:
                    date_from = None
                unit.journal.last_stat = self.get_state_summary(date_from)
                unit.journal.save()

    def set_record_data(self, data, record_id=None):
        if record_id:
            rec = Record.objects.get(pk=record_id)
            changed_fields = []
            for name in STANDARD_STATE_DATA:
                if rec.__getattribute__(name) != data[name]:
                    changed_fields.append(name)
                    rec.__setattr__(name, data[name])
            if self.extended_stat:
                rec.stateitem_set.all().delete()
                for state_name in EXT_STATE_DATA:
                    if data[state_name]:
                        rec.stateitem_set.create(
                            state=state_name,
                            time_in_state=data[state_name])
            rec.save(update_fields=changed_fields)
        else:
            rec = self.record_set.create(
                date=data['date'],
                work=data['work'],
                ostanov_cnt=data['ostanov_cnt'],
                pusk_cnt=data['pusk_cnt'],)
            if self.extended_stat:
                for state_name in EXT_STATE_DATA:
                    if data[state_name]:
                        rec.stateitem_set.create(
                            state=state_name,
                            time_in_state=data[state_name])
        self.update_state_cache()
        return rec

    def delete_record(self, record_id):
        rec = self.record_set.get(pk=record_id)
        rec.delete()
        self.update_state_cache()

    def get_last_records(self, depth=10):
        if self.stat_by_parent:
            return self.equipment.plant.journal.get_last_records(depth)
        else:
            return self.record_set.order_by('-date')[:depth]

    def set_event_data(self, data):
        self.eventitem_set.create(
            date=data['date'],
            event=data['event'])


class Record(models.Model):
    """
    Модель Одна строка стандартной записи журнала на дату начала периода
    """

    journal = models.ForeignKey('Journal', on_delete=models.CASCADE)
    date = models.DateField()
    work = models.DurationField(default='00:00')
    pusk_cnt = models.IntegerField(default=0)
    ostanov_cnt = models.IntegerField(default=0)

    def __str__(self):
        return "{0} work time: {1}".format(
            self.date,
            self.work)

    def ext_state(self, state_abr):
        try:
            res = self.stateitem_set.get(state=state_abr).time_in_state
        except ObjectDoesNotExist:
            res = timedelta(seconds=0)
        return res

    def reserv(self):
        return self.ext_state('RSV')

    def tek_rem(self):
        return self.ext_state('TRM')

    def av_rem(self):
        return self.ext_state('ARM')

    def kap_rem(self):
        return self.ext_state('KRM')

    def sr_rem(self):
        return self.ext_state('SRM')

    def reconstr(self):
        return self.ext_state('RCD')

    class Meta:
        default_permissions = []

RESERV = 'RSV'
TEK_REM = 'TRM'
AV_REM = 'ARM'
KAP_REM = 'KRM'
SR_REM = 'SRM'
RECONSTRUCTION = 'RCD'
STATE_CHOICES = (
    (RESERV, 'Резерв'),
    (TEK_REM, 'Тек. ремонт'),
    (AV_REM, 'Ав. ремонт'),
    (KAP_REM, 'Кап. ремонт'),
    (SR_REM, 'Сред. ремонт'),
    (RECONSTRUCTION, 'Реконструкция'),
)


class StateItem(models.Model):
    """
    Модель расширения стандартной записи статистики дополнительным,
    ненулевым, временем нахождения в состоянии
    """

    record = models.ForeignKey('Record', on_delete=models.CASCADE)
    state = models.CharField(max_length=3,
                             choices=STATE_CHOICES,
                             default=RESERV,
                             db_index=True)
    time_in_state = models.DurationField()

    class Meta:
        default_permissions = []


VVOD = 'VVD'
ZAMENA = 'ZMN'
SPISANIE = 'SPS'
EVENT_CHOICES = ((VVOD, 'Ввод'),
                 (ZAMENA, 'Замена'),
                 (SPISANIE, 'Списание'))
EVENT_CHOICES_DICT = dict(EVENT_CHOICES)


class EventItem(models.Model):
    """
    Модель Отражение события жизненного цикла
    из предопределенного набора: [Ввод, Списание, Замена]
    Например: ОиЖ | 01.03.2015 | Замена
    """

    journal = models.ForeignKey('Journal', on_delete=models.CASCADE)
    date = models.DateField()
    event = models.CharField(max_length=3,
                             choices=EVENT_CHOICES)
