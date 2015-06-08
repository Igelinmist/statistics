from django.test import TestCase
import datetime

from statistics.models import Journal
from catalog.models import Unit


def create_record(eq_name='Test equipment', ext_stat=False):
    eq = Unit(name=eq_name)
    eq.save()
    journal = Journal(equipment_id=eq.id, extended_stat=ext_stat)
    journal.save()
    rec = journal.record_set.create(
        date=datetime.date.today()-datetime.timedelta(days=1),
        pusk_cnt=1,
        ostanov_cnt=1,
        work=datetime.timedelta(hours=5),
        period_length=24,)
    if ext_stat:
        rec.stateitem_set.create(
            state='ARM',
            time_in_state=datetime.timedelta(hours=19))
    return rec


class JournalModelTest(TestCase):

    def test_get_data_for_new_record(self):
        '''
        Проверка подготовки данных для формы новой записи
        Должен возвращать None
        '''
        form_data = Journal.get_data()

        self.assertEqual(form_data, None)

    def test_get_data_form_existing_short_record(self):
        '''
        Проверка подготовки данных для формы существующей короткой записи
        Должен возвращать данные для полей
        '''
        rec = create_record()
        form_data = Journal.get_data(rec.id)

        self.assertEqual(
            form_data,
            {'date': datetime.date.today()-datetime.timedelta(days=1),
             'period_length': 24,
             'work': datetime.timedelta(hours=5),
             'pusk_cnt': 1,
             'ostanov_cnt': 1})

    def test_get_data_form_existing_full_record(self):
        '''
        Проверка подготовки данных для формы существующей полной записи
        Должен возвращать данные для полей
        '''
        rec = create_record(ext_stat=True)
        form_data = Journal.get_data(rec.id)
        emty_time = datetime.timedelta(hours=0)
        self.assertEqual(
            form_data, {
                'arm': datetime.timedelta(hours=19),
                'date': datetime.date.today()-datetime.timedelta(days=1),
                'krm': emty_time,
                'ostanov_cnt': 1,
                'period_length': 24,
                'rcd': emty_time,
                'pusk_cnt': 1,
                'rsv': emty_time,
                'srm': emty_time,
                'trm': emty_time,
                'work': datetime.timedelta(hours=5),
            })
