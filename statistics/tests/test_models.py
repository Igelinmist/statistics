from django.test import TestCase
import datetime

from statistics.models import Journal
from catalog.models import Unit


def create_journal(eq_name='Test equipment', ext_stat=False):
    eq = Unit(name=eq_name)
    eq.save()
    journal = Journal(equipment=eq, extended_stat=ext_stat)
    journal.save()
    return journal


def create_record(eq_name='Test equipment', ext_stat=False):
    journal = create_journal(eq_name, ext_stat)
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

        Тестируется метод get_data
        '''
        form_data = Journal.get_data()

        self.assertEqual(form_data, None)

    def test_get_data_form_existing_short_record(self):
        '''
        Проверка подготовки данных для формы существующей короткой записи
        Должен возвращать данные для полей

        Тестируется метод get_data
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

        Тестируется метод get_data
        '''
        rec = create_record(ext_stat=True)
        form_data = Journal.get_data(rec.id)
        empty_time = datetime.timedelta(hours=0)
        self.assertEqual(
            form_data, {
                'arm': datetime.timedelta(hours=19),
                'date': datetime.date.today()-datetime.timedelta(days=1),
                'krm': empty_time,
                'ostanov_cnt': 1,
                'period_length': 24,
                'rcd': empty_time,
                'pusk_cnt': 1,
                'rsv': empty_time,
                'srm': empty_time,
                'trm': empty_time,
                'work': datetime.timedelta(hours=5),
            })

    def test_set_data_for_new_full_record(self):
        '''
        Проверка создания новой записи по данным, полученным из формы
        для полной записи статистики

        Тестируется метод set_data
        '''
        empty_time = datetime.timedelta(hours=0)
        form_data = {
            'date': datetime.date.today()-datetime.timedelta(days=1),
            'period_length': 24,
            'ostanov_cnt': 1,
            'pusk_cnt': 1,
            'work': datetime.timedelta(hours=5),
            'rsv': empty_time,
            'trm': empty_time,
            'arm': datetime.timedelta(hours=19),
            'krm': empty_time,
            'srm': empty_time,
            'rcd': empty_time,
        }
        journal = create_journal(ext_stat=True)
        rec = journal.set_data(form_data)

        self.assertEqual(journal.record_set.count(), 1)
        self.assertEqual(rec.stateitem_set.count(), 1)

    def test_set_data_for_new_short_record(self):
        '''
        Проверка создания новой записи по данным, полученным из формы
        для короткой записи статистики
        Тестируется метод set_data
        '''
        form_data = {
            'date': datetime.date.today()-datetime.timedelta(days=1),
            'period_length': 24,
            'ostanov_cnt': 1,
            'pusk_cnt': 1,
            'work': datetime.timedelta(hours=5),
        }
        journal = create_journal(ext_stat=False)
        rec = journal.set_data(form_data)

        self.assertEqual(journal.record_set.count(), 1)
        self.assertEqual(rec.stateitem_set.count(), 0)
