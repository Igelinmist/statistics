from django.db import models

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

    def get_record(self, data):
        new_record = self.record_set.create(
            date=data['rec_date'],
            work=data['work'],
            period_length=int(data['rec_period']),
            pusk_cnt=int(data['starts']),
            ostanov_cnt=int(data['stops']),
        )
        new_record.stateitem_set.create(
            state='RSV',
            time_in_state=data['reserv'],
        )


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
