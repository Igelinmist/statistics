from django.test import TestCase
from datetime import date, timedelta

from statistics.models import Journal
from statistics.tests import factories


class JournalModelTest(TestCase):

    def test_get_record_data_for_new_record(self):
        '''
        Для новой записи набор данных пустой\
        (get_record_data(record_id=None))
        '''
        form_data = Journal.get_record_data()

        self.assertEqual(form_data, None)

    def test_new_record_creation(self):
        '''
        Новая запись создается по данным формы\
        (set_record_data(data, record_id=None, process_ext_states=True))
        '''
        journal = factories.prepare_journal_tree()['full_journal']
        journal.set_record_data(factories.form_data())

        self.assertEqual(journal.record_set.count(), 1)

    def test_update_stat_on_new_record_creation(self):
        '''
        Создание новой записи обновляет статистику\
        (update_state_cache())
        '''
        journal = factories.prepare_journal_tree()['full_journal']
        journal.set_record_data(factories.form_data())

        self.assertEqual(journal.last_stat, 'wd=5:00,psk=1,ost=1')

    def test_update_stat_on_delete_record(self):
        '''
        Удаление записи обновляет статистику\
        (update_state_cache())
        '''
        journal = factories.prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(factories.form_data())
        journal.delete_record(rec.id)

        self.assertEqual(journal.last_stat, 'wd=00:00,psk=0,ost=0')

    def test_add_additional_state_on_record_creation(self):
        '''
        Новая запись с состоянием аварийного ремонта добавляет в базу\
        state_item запись
        '''
        journal = factories.prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(factories.form_data())

        self.assertEqual(rec.stateitem_set.count(), 1)

    def test_get_record_data_form_existing_short_record(self):
        '''
        Подготовка данных для формы редактирования существующей записи\
        (set_record_data(data, record_id=None, process_ext_states=True))
        '''
        journal = factories.prepare_journal_tree()['base_journal']
        rec = journal.set_record_data(factories.form_data())
        form_data = Journal.get_record_data(rec.id)

        self.assertEqual(
            form_data,
            {'date': date.today()-timedelta(days=1),
             'work': timedelta(hours=5),
             'pusk_cnt': 1,
             'ostanov_cnt': 1})

    def test_get_record_data_form_existing_full_record(self):
        '''
        Подготовка данных для формы на базе существующей записи\
        (get_record_data(record_id=None))
        '''
        journal = factories.prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(factories.form_data())
        form_data = Journal.get_record_data(rec.id)

        self.assertEqual(
            form_data,
            {'date': date.today()-timedelta(days=1),
             'work': timedelta(hours=5),
             'arm': timedelta(hours=19),
             'trm': timedelta(0),
             'krm': timedelta(0),
             'rsv': timedelta(0),
             'srm': timedelta(0),
             'rcd': timedelta(0),
             'pusk_cnt': 1,
             'ostanov_cnt': 1})

    # def test_prepare_base_report_data(self):
    #     """
    #     Подготовка основного массива отчетных данных для технологического узла
    #     """
    #     equipment = factories.prepare_journal_tree()['unit_root']
    #     report = factories.ReportFactory(equipment_id=equipment.id)
    #     factories.ColumnFactory(
    #         report_id=report.id,
    #         title='Наработка с ввода/замены',
    #         column_type='ITV',
    #         from_event='FVZ'
    #     )
    #     #TODO для замены надо сделать отдельный тест
    #     report_table = report.prepare_report_data()

    #     self.assertEqual(
    #         report_table,
    #         [
    #             ['Оборудование', 'subunit1', 'subunit2'],
    #             ['Наработка с ввода/замены', '72:00', '72:00'],
    #             ['Число пусков', 3, 3],
    #         ]
    #     )

    def test_prepare_journals_id_for_report(self):
        """
        Преподготовка данных для отчета - таблица с номерами журналов\
        prepare_journals_id_for_report(self)
        """
        journal_tree = factories.prepare_journal_tree()
        equipment = journal_tree['unit_root']
        report = factories.ReportFactory(equipment_id=equipment.id)
        factories.ColumnFactory(
            report_id=report.id,
            title='Наработка с ввода/замены',
            column_type='ITV',
            from_event='FVZ'
        )
        factories.ColumnFactory(
            report_id=report.id,
            title='Кол-во пусков',
            column_type='PCN',
            from_event='FVZ'
        )

        ids_table = report.prepare_journals_id_for_report()

        self.assertEqual(
            ids_table,
            [
                [journal_tree['journal1'].id, journal_tree['journal1'].id],
                [journal_tree['journal2'].id, journal_tree['journal2'].id],
            ])

    def test_prepare_journals_id_for_report_with_subunit(self):
        """
        Преподготовка данных для отчета - таблица с номерами журналов, включая подоборудование\
        prepare_journals_id_for_report(self)
        """
        journal_tree = factories.prepare_journal_tree()
        equipment = journal_tree['unit_root']
        report = factories.ReportFactory(equipment_id=equipment.id)
        factories.ColumnFactory(
            report_id=report.id,
            title='Наработка с ввода/замены',
            column_type='ITV',
            from_event='FVZ'
        )
        factories.ColumnFactory(
            report_id=report.id,
            title='Наработка detail1',
            column_type='ITV',
            from_event='FVZ',
            element_name_filter='detail1',
            weigh=2,
        )

        ids_table = report.prepare_journals_id_for_report()

        self.assertEqual(
            ids_table,
            [
                [journal_tree['journal1'].id,
                 journal_tree['detail11'].journal.id],
                [journal_tree['journal2'].id,
                 journal_tree['detail21'].journal.id],
            ])

    def test_prepare_journals_id_for_report_with_subunit_included_in_part(self):
        """
        Преподготовка данных для отчета - таблица с номерами журналов, включая подоборудование, но не у всех\
        prepare_journals_id_for_report(self)
        """
        journal_tree = factories.prepare_journal_tree()
        equipment = journal_tree['unit_root']
        report = factories.ReportFactory(equipment_id=equipment.id)
        factories.ColumnFactory(
            report_id=report.id,
            title='Наработка с ввода/замены',
            column_type='ITV',
            from_event='FVZ'
        )
        factories.ColumnFactory(
            report_id=report.id,
            title='Наработка detail2',
            column_type='ITV',
            from_event='FVZ',
            element_name_filter='detail2',
            weigh=2,
        )

        ids_table = report.prepare_journals_id_for_report()

        self.assertEqual(
            ids_table,
            [
                [journal_tree['journal1'].id,
                 journal_tree['detail12'].journal.id],
                [journal_tree['journal2'].id,
                 None],
            ])
