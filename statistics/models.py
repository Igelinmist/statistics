from django.db import models


def default_stat():
    return {"wd": "00:00", "psk": 0, "ost": 0}


class Journal(models.Model):
    """
    Description: Раздел журнала для группировки записей статистики
    по конкретному оборудованию
    """

    equipment = models.ForeignKey('catalog.Unit')
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


class JournalLine(models.Model):
    """
    Description: Одна строка записи журнала на дату начала периода
    """
    DAY = 24
    YEAR = 8760
    LEAP_YEAR = 8784
    PERIOD_IN_CHOICES = (
        (DAY, 'Сутки'),
        (YEAR, 'Год'),
        (LEAP_YEAR, 'Вис. год'),
    )

    journal = models.ForeignKey('Journal')
    date = models.DateField()
    period_length = models.IntegerField(choices=PERIOD_IN_CHOICES,
                                        default=DAY)
    pusk_cnt = models.IntegerField(default=0)
    ostanov_cnt = models.IntegerField(default=0)


class StateItem(models.Model):
    """
    Description: Ненулевая позиция состояния Оборудования из Журнала.
    Например: ЗЖ | 24:00 | Работа
    """
    WORK = 'WRK'
    RESERV = 'RSV'
    TEK_REM = 'TRM'
    AV_REM = 'ARM'
    KAP_REM = 'KRM'
    SR_REM = 'SRM'
    RECONSTRUCTION = 'RCD'
    STATE_CHOICES = (
        (WORK, 'Работа'),
        (RESERV, 'Резерв'),
        (TEK_REM, 'Тек. ремонт'),
        (AV_REM, 'Ав. ремонт'),
        (KAP_REM, 'Кап. ремонт'),
        (SR_REM, 'Сред. ремонт'),
        (RECONSTRUCTION, 'Реконструкция'),
    )

    journal_line = models.ForeignKey('JournalLine')
    state = models.CharField(max_length=3,
                             choices=STATE_CHOICES,
                             default=WORK,
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
