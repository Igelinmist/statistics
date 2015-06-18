from datetime import timedelta

from django.db import models

from catalog.models import Unit


STANDARD_STATE_DATA = ('date', 'work', 'period_length',
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
    Класс Журнала записей статистики
    по конкретному оборудованию
    """

    equipment = models.OneToOneField(Unit)
    extended_stat = models.BooleanField(default=False)
    stat_by_parent = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    last_stat = models.CharField(max_length=250,
                                 default=default_stat,
                                 editable=False)

    class Meta:
        ordering = ['equipment__name']

    def __str__(self):
        return self.equipment.name

    def get_record_data(record_id=None):
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
        plant_equipment = self.equipment
        for unit in plant_equipment.unit_set.all():
            if unit.journal and unit.journal.stat_by_parent:
                try:
                    date_from = unit.journal.eventitem_set.filter(event='ZMN').order_by('-date')[0].date
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
                period_length=data['period_length'],
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

    def get_last_records(self, depth=10):
        if self.stat_by_parent:
            return self.equipment.plant.journal.get_last_records(depth)
        else:
            return self.record_set.order_by('-date')[:depth]

    def set_event_data(self, data):
        self.eventitem_set.create(
            date=data['date'],
            event=data['event'])

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
    Класс Одна строка стандартной записи журнала на дату начала периода
    """

    journal = models.ForeignKey('Journal')
    date = models.DateField()
    period_length = models.IntegerField(choices=PERIOD_IN_CHOICES,
                                        default=DAY)
    work = models.DurationField(default='00:00')
    pusk_cnt = models.IntegerField(default=0)
    ostanov_cnt = models.IntegerField(default=0)

    def __del__(self):
        journal = self.journal
        del self
        journal.update_state_cache()

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
    Класс расширения стандартной записи статистики дополнительным,
    ненулевым, временем нахождения в состоянии
    """

    record = models.ForeignKey('Record')
    state = models.CharField(max_length=3,
                             choices=STATE_CHOICES,
                             default=RESERV,
                             db_index=True)
    time_in_state = models.DurationField()


VVOD = 'VVD'
ZAMENA = 'ZMN'
SPISANIE = 'SPS'
EVENT_CHOICES = ((VVOD, 'Ввод'),
                 (ZAMENA, 'Замена'),
                 (SPISANIE, 'Списание'))
EVENT_CHOICES_DICT = dict(EVENT_CHOICES)


class EventItem(models.Model):
    """
    Description: Отражение события жизненного цикла
    из предопределенного набора: [Ввод, Списание, Замена]
    Например: ОиЖ | 01.03.2015 | Замена
    """

    journal = models.ForeignKey('Journal')
    date = models.DateField()
    event = models.CharField(max_length=3,
                             choices=EVENT_CHOICES)
