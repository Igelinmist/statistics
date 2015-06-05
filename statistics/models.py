from django.db import models
from datetime import timedelta

from catalog.models import Unit


def default_stat():
    return {"wd": "00:00", "psk": 0, "ost": 0}


class Journal(models.Model):
    """
    Description: Раздел журнала для группировки записей статистики
    по конкретному оборудованию
    """

    equipment = models.OneToOneField(Unit)
    extended_stat = models.BooleanField(default=False)
    stat_by_parent = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    last_stat = models.CharField(max_length=100,
                                 default=default_stat,
                                 editable=False)

    class Meta:
        ordering = ['equipment__name']

    def __str__(self):
        return self.equipment.name

    def get_data(record_id=None):
        data = {}
        if record_id:
            rec = Record.objects.get(pk=record_id)
            for name in ('date', 'work', 'period_length',
                         'ostanov_cnt', 'pusk_cnt'):
                data[name] = rec.__getattribute__(name)
            if rec.journal.extended_stat:
                for state in ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
                    data[state] = timedelta(seconds=0)
                for state_item in rec.stateitem_set.all():
                    data[state_item.state.lower()] = state_item.time_in_state
            return data
        else:
            return None

    def set_data(journal, data, record_id=None):
        if record_id:
            rec = Record.objects.get(pk=record_id)
            changed_fields = []
            for name in ('date', 'work', 'period_length',
                         'ostanov_cnt', 'pusk_cnt'):
                if rec.__getattribute__(name) != data[name]:
                    changed_fields.append(name)
                    rec.__setattr__(name, data[name])
            if journal.extended_stat:
                rec.stateitem_set.all().delete()
                for state_name in ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
                    if data[state_name]:
                        rec.stateitem_set.create(
                            state=state_name,
                            time_in_state=data[state_name])
            rec.save(update_fields=changed_fields)
        else:
            new_record = journal.record_set.create(
                date=data['date'],
                period_length=data['period_length'],
                work=data['work'],
                ostanov_cnt=data['ostanov_cnt'],
                pusk_cnt=data['pusk_cnt'],)
            if journal.extended_stat:
                 for state_name in ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
                    if data[state_name]:
                        new_record.stateitem_set.create(
                            state=state_name,
                            time_in_state=data[state_name])


DAY = 24
YEAR = 8760
LEAP_YEAR = 8784
PERIOD_IN_CHOICES = (
    (DAY, 'Сутки'),
    (YEAR, 'Год'),
    (LEAP_YEAR, 'Вис. год'),
)


class Record(models.Model):
    """
    Description: Одна строка записи журнала на дату начала периода
    """

    journal = models.ForeignKey('Journal')
    date = models.DateField()
    period_length = models.IntegerField(choices=PERIOD_IN_CHOICES,
                                        default=DAY)
    work = models.DurationField(default='00:00')
    pusk_cnt = models.IntegerField(default=0)
    ostanov_cnt = models.IntegerField(default=0)

    def __str__(self):
        return "{0} | {1} | {2}".format(
            self.date,
            self.period_length,
            self.work)

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
    Description: Ненулевая позиция состояния Оборудования из Журнала.
    Например: ЗЖ | 24:00 | Работа
    """

    record = models.ForeignKey('Record')
    state = models.CharField(max_length=3,
                             choices=STATE_CHOICES,
                             default=RESERV,
                             db_index=True)
    time_in_state = models.DurationField()


class EventItem(models.Model):
    """
    Description: Отражение события жизненного цикла
    из предопределенного набора: [Ввод, Списание, Замена]
    Например: ОиЖ | 01.03.2015 | Замена
    """
    VVOD = 'VVD'
    ZAMENA = 'ZMN'
    SPISANIE = 'SPS'
    EVENT_CHOICES = ((VVOD, 'Ввод'),
                     (ZAMENA, 'Замена'),
                     (SPISANIE, 'Списание'))

    journal = models.ForeignKey('Journal')
    date = models.DateField()
    event = models.CharField(max_length=3,
                             choices=EVENT_CHOICES)
