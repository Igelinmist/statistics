from datetime import timedelta, datetime, date
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from catalog.models import Unit
from statistics.helpers import default_stat, stat_timedelta, stat_timedelta_for_report, reqdate


STATE_CHOICES = (
    ('RSV', 'Резерв'),
    ('TRM', 'Тек. ремонт'),
    ('ARM', 'Ав. ремонт'),
    ('KRM', 'Кап. ремонт'),
    ('SRM', 'Сред. ремонт'),
    ('RCD', 'Реконструкция'),
)

EVENT_CHOICES = (
    ('VVD', 'Ввод'),
    ('VKR', 'Ввод из капремонта'),
    ('VSR', 'Ввод из ср. ремонта'),
    ('VRC', 'Ввод из реконструкции'),
    ('ZMN', 'Ввод после замены'),
    ('SPS', 'Списание'),
)
EVENT_CHOICES_DICT = dict(EVENT_CHOICES)

STANDARD_STATE_DATA = ('date', 'work', 'ostanov_cnt', 'pusk_cnt')

EXT_STATE_DATA = ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd')


class Journal(models.Model):
    """
    Модель Журнала записей статистики
    по конкретному оборудованию
    """

    equipment = models.OneToOneField(Unit, on_delete=models.CASCADE, related_name='journal')
    extended_stat = models.BooleanField(default=False)
    stat_by_parent = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    last_stat = models.CharField(max_length=250,
                                 default=default_stat,
                                 editable=False)

    class Meta:
        ordering = ['equipment__name']
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'
        default_permissions = []
        permissions = (
            ('view_journal_details', 'Может просматривать записи журнала'),
            ('view_journal_list', 'Может посмотреть список журналов'),
            ('create_journal_record', 'Может создать запись в журнале'),
            ('edit_journal_record', 'Может редактировать запись в журнале'),
            ('delete_journal_record', 'Может удалить запись в журнале'),
            ('create_journal_event', 'Может создать событие в журнале'),
            ('delete_journal_event', 'Может удалить событие в журнале'),
        )

    def unit_get_journal(unit):
        try:
            return unit.journal
        except Journal.DoesNotExist:
            return None

    def unit_has_journal(unit):
        try:
            if unit.journal:
                return True
        except Journal.DoesNotExist:
            return False

    def get_journals_work_on_dates(root_unit, start_date, days_cnt):
        """
        Метод класса Journal предназначен для страницы мультижурнального
        ввода продолжительности работы оборудования для мультидат.
        Метод формирует таблицу текущего состояния по введенным данным
        """
        res = []
        unit_tree = root_unit.unit_tree()
        # получаем словарь словарей имеющихся записей для журналов
        wd = Record.get_records_on_dates(unit_tree, start_date, days_cnt)
        res.append(wd['dates'])
        # для каждой единицы оборудования в дереве
        for unit, ident in unit_tree:
            if Journal.unit_has_journal(unit):
                if unit.journal.stat_by_parent:
                    continue
                jstr = ['--' * ident + unit.name]
                # для каждой даты (формат "дд.мм.ГГГГ")
                for dkey in wd['dates']:
                    jkey = str(unit.journal.id)
                    if dkey in wd[jkey].keys():
                        jstr.append(wd[jkey][dkey])
                    else:
                        jstr.append('-')
                res += [jstr]
            else:
                res.append(['--' * ident + unit.name])
        return res

    def __str__(self):
        plant_name = self.equipment.plant.name if self.equipment.plant else '-'
        return plant_name + ' \ ' + self.equipment.name


# Текущий конец рефакторинга для методов объектов Journal
# *******************************************************


    def get_record_data(self, record_id=None, rdate=None):
        """
        Description: Метод получения данных для инициализации полей формы
        существующей записью, включая расширенные состояния при наличии
        """
        if not record_id and rdate:
            try:
                record_id = self.record_set.filter(date=rdate)[0].id
            except IndexError:
                return None
        if record_id:
            data = {}
            rec = self.record_set.get(pk=record_id)
            data['date'] = rec.date.strftime('%d.%m.%Y')
            data['work'] = stat_timedelta(rec.work)
            data['pusk_cnt'] = rec.pusk_cnt
            data['ostanov_cnt'] = rec.ostanov_cnt
            if self.extended_stat:
                # сначала инициализация всего набора
                for state in EXT_STATE_DATA:
                    data[state] = '0:00'
                # потом ненулевых состояний
                for state_item in rec.stateitem_set.all():
                    data[state_item.state.lower()] = stat_timedelta(state_item.time_in_state)
            return data
        else:
            return None





    def rec_on_date(self, dt):
        """
        Дата преобразуется в формат для запроса.
        Результат метода либо запись, либо None
        """
        req_date = reqdate(dt)
        try:
            return self.record_set.filter(date=req_date).all()[0]
        except IndexError:
            return None

    def get_state_summary(self, date_from=None, date_to=None):
        """
        Description: Метод подсчета базовой статистики, возможно,
        от определенной даты
        """
        if self.record_set.count():
            recs = self.record_set
            if date_from:
                recs = recs.filter(date__gte=date_from)
            if date_to:
                recs = recs.exclude(date__gte=date_to)
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

    def set_record_data(self, data, record_id=None, process_ext_states=True):
        # Если не задан номер записи для изменения надо проверить дублирование
        if not record_id:
            try:
                record_id = self.record_set.filter(date=data['date']).all()[0].id
            except IndexError:
                # точно нет записи - создаем
                rec = self.record_set.create(
                    date=data['date'],
                    work=data['work'],
                    ostanov_cnt=data['ostanov_cnt'],
                    pusk_cnt=data['pusk_cnt'],)
                if self.extended_stat and process_ext_states:
                    for state_name in EXT_STATE_DATA:
                        if data[state_name]:
                            rec.stateitem_set.create(
                                state=state_name.upper(),
                                time_in_state=data[state_name])
                self.update_state_cache()
                return rec
        rec = Record.objects.get(pk=record_id)
        changed_fields = []
        for name in STANDARD_STATE_DATA:
            if rec.__getattribute__(name) != data[name]:
                changed_fields.append(name)
                rec.__setattr__(name, data[name])
        if self.extended_stat and process_ext_states:
            rec.stateitem_set.all().delete()
            for state_name in EXT_STATE_DATA:
                if data[state_name]:
                    rec.stateitem_set.create(
                        state=state_name.upper(),
                        time_in_state=data[state_name])
        rec.save(update_fields=changed_fields)
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

    def get_journal_or_subjournal_id(self, subunit_name=None):
        if subunit_name:
            unit = self.equipment
            try:
                subunit = unit.unit_set.filter(name=subunit_name)[0]
                return subunit.journal.id if subunit.journal else None
            except IndexError:
                return None
        else:
            return self.id

    def get_report_cell(self, summary_type='ITV',
                        from_event='FVZ', date_to=None):
        journal = self.equipment.plant.journal if self.stat_by_parent else self
        from_event_to_event_dict = {
            'FVZ': 'ZMN',
            'FKR': 'VKR',
            'FSR': 'VSR',
            'FRC': 'VRC',
        }
        if journal.record_set.count():
            try:
                date_from = self.eventitem_set.filter(
                    event=from_event_to_event_dict[from_event]
                ).order_by('-date')[0].date
                if summary_type == 'DT':
                    return date_from.strftime("%d.%m.%Y")
            except IndexError:
                date_from = None
                if from_event != 'FVZ':
                    return '-'
                elif summary_type == 'DT':
                    return '-'

            recs = journal.record_set
            if date_from:
                # Время "от события" откатываем на месяц назад, поскольку
                # капитальный и средный ремонты, замены и реконструкции
                # длятся не менее месяца, а раньше интервалы фиксировались
                # за месяц или год, что приводит к неверному расчету
                recs = recs.filter(date__gte=date_from - timedelta(days=31))
            if date_to:
                recs = recs.exclude(date__gte=date_to)
            if summary_type == 'PCN':
                return recs.aggregate(models.Sum('pusk_cnt'))['pusk_cnt__sum']
            elif summary_type == 'OCN':
                return recs.aggregate(
                    models.Sum('ostanov_cnt'))['ostanov_cnt__sum']
            else:
                return stat_timedelta_for_report(
                    recs.aggregate(models.Sum('work'))['work__sum']
                )
        else:
            if summary_type in ('PCN', 'OCN'):
                return 0
            elif summary_type == 'dt':
                return '-'
            else:
                return '00:00'


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

    def get_records_on_date(request_date):
        if request_date:
            try:
                slice_date = datetime.strptime(
                    request_date,
                    "%d.%m.%Y")
            except ValueError:
                slice_date = (date.today() - timedelta(days=1))
        else:
            slice_date = (date.today() - timedelta(days=1))
        query_date = slice_date.strftime("%Y-%m-%d")

        records = Record.objects.filter(date=query_date).values(
            'journal_id',
            'work',
            'id',
        )
        res_dict = {
            rec['journal_id']: (rec['work'], rec['id']) for rec in records
        }
        res_dict['date'] = slice_date
        return res_dict

    def get_records_on_dates(unit_tree, start_date, days_cnt):
        """
        Метод класса Record готовит словарь словарей наработки оборудования
        из журналов (тех, что имеют статистику) на даты для дерева оборудования
        """
        res = {}
        date_list = [
            (start_date + timedelta(days=dc)).strftime("%Y-%m-%d")
            for dc in range(days_cnt)
        ]
        res.update(dict(dates=date_list))
        recordsDataSet = Record.objects.filter(date__in=date_list)
        for uitem, ident in unit_tree:
            try:
                journal_key = str(uitem.journal.id)
                work_on_dates_dict = {}
                for rec in recordsDataSet.filter(journal_id=uitem.journal.id).all():
                    date_key = rec.date.strftime("%Y-%m-%d")
                    work_on_dates_dict.update({date_key: stat_timedelta(rec.work)})
                res.update({journal_key: work_on_dates_dict})
            except Journal.DoesNotExist:
                continue
        return res

    def get_data(self):
        """
        Метод подготовки всех данных записи и выдачи в виде словаря.
        Продолжительность приведена в строках
        """
        rec_data = {'record_id': self.id}
        for name in STANDARD_STATE_DATA:
            rec_data[name] = self.__getattribute__[name]
        rec_data.update(dict.fromkeys(EXT_STATE_DATA, '0:00'))
        for ext_state in self.stateitem_set.all():
            rec_data[ext_state.state.lower()] = stat_timedelta(ext_state.time_in_state)
        return rec_data

    class Meta:
        default_permissions = []
        verbose_name = 'запись'
        verbose_name_plural = 'записи'


class StateItem(models.Model):
    """
    Модель расширения стандартной записи статистики дополнительным,
    ненулевым, временем нахождения в состоянии
    """

    record = models.ForeignKey('Record', on_delete=models.CASCADE)
    state = models.CharField(max_length=3,
                             choices=STATE_CHOICES,
                             default='RSV',
                             db_index=True)
    time_in_state = models.DurationField()

    class Meta:
        default_permissions = []


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
