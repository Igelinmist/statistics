from django.test import TestCase

from statistics.models import Journal
from statistics.tests import factories


class JournalModelTest(TestCase):

    def test_get_test_unit_tree(self):
        """
        Equipment/Journal tree generator testing
        """

        factories.prepare_journal_tree()

        self.assertEqual(Journal.objects.count(), 6)

    def test_new_record_creation(self):
        '''
        Record creation testing
        '''

        journal = factories.prepare_journal_tree()['full_journal']
        journal.set_record_data(factories.form_data())

        self.assertEqual(journal.record_set.count(), 1)

    def test_update_stat_on_new_record_creation(self):
        '''
        Record stat update on creation testing
        '''

        journal = factories.prepare_journal_tree()['full_journal']
        journal.set_record_data(factories.form_data())

        self.assertEqual(journal.last_stat, 'wd=5:00,psk=1,ost=1')

    def test_add_additional_state_on_record_creation(self):
        '''
        Record add state_item on creation testing
        '''

        journal = factories.prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(factories.form_data())

        self.assertEqual(rec.stateitem_set.count(), 1)

    # def test_get_record_data_form_existing_short_record(self):
    #     '''
    #     Проверка подготовки данных для формы существующей короткой записи
    #     Должен возвращать данные для полей

    #     Тестируется метод get_record_data
    #     '''
    #     rec = create_record()
    #     form_data = Journal.get_record_data(rec.id)

    #     self.assertEqual(
    #         form_data,
    #         {'date': datetime.date.today()-datetime.timedelta(days=1),
    #          'period_length': 24,
    #          'work': datetime.timedelta(hours=5),
    #          'pusk_cnt': 1,
    #          'ostanov_cnt': 1})

    # def test_get_record_data_form_existing_full_record(self):
    #     '''
    #     Проверка подготовки данных для формы существующей полной записи
    #     Должен возвращать данные для полей

    #     Тестируется метод get_record_data
    #     '''
    #     rec = create_record(ext_stat=True)
    #     form_data = Journal.get_record_data(rec.id)
    #     empty_time = datetime.timedelta(hours=0)
    #     self.assertEqual(
    #         form_data, {
    #             'arm': datetime.timedelta(hours=19),
    #             'date': datetime.date.today()-datetime.timedelta(days=1),
    #             'krm': empty_time,
    #             'ostanov_cnt': 1,
    #             'period_length': 24,
    #             'rcd': empty_time,
    #             'pusk_cnt': 1,
    #             'rsv': empty_time,
    #             'srm': empty_time,
    #             'trm': empty_time,
    #             'work': datetime.timedelta(hours=5),
    #         })
