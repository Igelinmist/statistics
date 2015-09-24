from django.test import TestCase
from datetime import date, timedelta

from statistics.models.report import Report
from statistics.models.journal import Journal
from statistics.tests import factories
from .helpers_foo import prepare_journal_tree, form_data
from .helpers_foo import prepare_test_data_and_report_conf
from .helpers_foo import prepare_test_data_and_report_conf_for_subjournal
from .helpers_foo import prepare_journal_tree_records
from .helpers_foo import prepare_journal_tree_records_report


class JournalModelTest(TestCase):

    def test_get_record_data_for_new_record(self):
        """
        Модель Journal передает пустой набор данных для новой записи в форму.
        """
        journal = prepare_journal_tree()['full_journal']
        form_data = journal.get_record_data()

        self.assertEqual(form_data, None)

    def test_new_record_creation(self):
        '''
        Модель Journal создает запись по данным POST формы\
        Журнал расширенной статистики.
        '''
        journal = prepare_journal_tree()['full_journal']
        journal.set_record_data(form_data())

        self.assertEqual(journal.record_set.count(), 1)

    def test_update_stat_on_new_record_creation(self):
        '''
        Модель Journal обновляет статистику.\
        При создании записи.
        '''
        journal = prepare_journal_tree()['full_journal']
        journal.set_record_data(form_data())

        self.assertEqual(journal.last_stat, 'wd=5:00,psk=1,ost=1')

    def test_update_stat_on_delete_record(self):
        '''
        Модель Journal обновляет статистику.\
        При удалении записи.
        '''
        journal = prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(form_data())
        journal.delete_record(rec.id)

        self.assertEqual(journal.last_stat, 'wd=00:00,psk=0,ost=0')

    def test_add_additional_state_on_record_creation(self):
        '''
        Модель Journal создает новую запись.\
        Создает новое состояние (state_item) расширенной статистики.
        '''
        journal = prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(form_data())

        self.assertEqual(rec.stateitem_set.count(), 1)

    def test_get_record_data_form_existing_short_record(self):
        '''
        Модель Journal готовит данные для формы редактирования существующей\
        короткой записи
        '''
        journal = prepare_journal_tree()['base_journal']
        rec = journal.set_record_data(form_data())
        fdata = journal.get_record_data(rec.id)

        self.assertEqual(
            fdata,
            {'date': date.today()-timedelta(days=1),
             'work': timedelta(hours=5),
             'pusk_cnt': 1,
             'ostanov_cnt': 1})

    def test_get_record_data_form_existing_full_record(self):
        """
        Модель Journal готовит данные для формы редактирования существующей\
        полной записи
        """
        journal = prepare_journal_tree()['full_journal']
        rec = journal.set_record_data(form_data())
        fdata = journal.get_record_data(rec.id)

        self.assertEqual(
            fdata,
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

    def test_get_report_cell_itv_from_vvod(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        число часов работы с ввода
        """
        journal_tree = prepare_test_data_and_report_conf(
            ctype='ITV'
        )['journal_tree']

        self.assertEqual(
            journal_tree['full_journal'].get_report_cell(from_event='FVZ'),
            '200'
        )

    def test_get_report_cell_itv_from_zamena(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        число часов работы с замены
        """
        test_journal = prepare_test_data_and_report_conf(
            fevent='FVZ',
            ctype='ITV'
        )['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(from_event='FVZ'),
            '100'
        )

    def test_get_report_cell_date_of_zamena(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        дата замены
        """
        test_data = prepare_test_data_and_report_conf(
            fevent='FVZ',
            ctype='DT'
        )
        test_journal = test_data['test_journal']
        edate = test_data['edate'].strftime("%d.%m.%Y")

        self.assertEqual(
            test_journal.get_report_cell(
                from_event='FVZ',
                summary_type='DT'),
            edate
        )

    def test_get_report_cell_date_of_zamena_without_event(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        дата замены, но замена отсутствует
        """
        test_data = prepare_test_data_and_report_conf(
            fevent='FVZ',
            ctype='DT',
            create_event=False,
        )
        test_journal = test_data['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(
                from_event='FVZ',
                summary_type='DT'),
            '-'
        )

    def test_get_report_cell_itv_from_srrem(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        число часов работы со среднего ремонта
        """
        test_journal = prepare_test_data_and_report_conf(
            fevent='FSR',
            ctype='ITV'
        )['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(from_event='FSR'),
            '100'
        )

    def test_get_report_cell_date_of_srrem(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        дата среднего ремонта
        """
        test_data = prepare_test_data_and_report_conf(
            fevent='FSR',
            ctype='DT'
        )
        test_journal = test_data['test_journal']
        edate = test_data['edate'].strftime("%d.%m.%Y")

        self.assertEqual(
            test_journal.get_report_cell(
                from_event='FSR',
                summary_type='DT'),
            edate
        )

    def test_get_report_cell_itv_from_kaprem(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        число часов работы с капремонта
        """
        test_journal = prepare_test_data_and_report_conf(
            fevent='FKR',
            ctype='ITV'
        )['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(from_event='FKR'),
            '100'
        )

    def test_get_report_cell_itv_from_kaprem_without_event(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        число часов работы с капремонта в отсутствии капремонта
        """
        test_journal = prepare_test_data_and_report_conf(
            fevent='FKR',
            ctype='ITV',
            create_event=False,
        )['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(from_event='FKR'),
            '-'
        )

    def test_get_report_cell_date_of_kaprem(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        дата капитального ремонта
        """
        test_data = prepare_test_data_and_report_conf(
            fevent='FKR',
            ctype='DT'
        )
        test_journal = test_data['test_journal']
        edate = test_data['edate'].strftime("%d.%m.%Y")

        self.assertEqual(
            test_journal.get_report_cell(
                from_event='FKR',
                summary_type='DT'),
            edate
        )

    def test_get_report_cell_pcn_from_vvod(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        кол-во пусков с ввода/замены
        """
        test_journal = prepare_test_data_and_report_conf(
            fevent='FVZ',
            ctype='PCN'
        )['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(
                summary_type='PCN',
                from_event='FVZ'
            ),
            5
        )

    def test_get_report_cell_ocn_from_vvod(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        кол-во остановов с ввода/замены
        """
        test_journal = prepare_test_data_and_report_conf(
            fevent='FVZ',
            ctype='OCN'
        )['test_journal']

        self.assertEqual(
            test_journal.get_report_cell(
                summary_type='OCN',
                from_event='FVZ'
            ),
            5
        )

    def test_get_report_cell_itv_from_vvod_for_subjournal(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        подчиненный журнал число часов работы с ввода
        """
        journal_tree = prepare_test_data_and_report_conf_for_subjournal(
            ctype='ITV'
        )['journal_tree']

        self.assertEqual(
            journal_tree['subjournal'].get_report_cell(from_event='FVZ'),
            '100'
        )

    def test_get_report_cell_itv_from_zamena_for_subjournal(self):
        """
        Модель Journal вычисляет отчетные данные для ячейки\
        подчиненный журнал число часов работы с замены
        """
        journal_tree = prepare_test_data_and_report_conf_for_subjournal(
            ctype='ITV',
            replaced=True
        )['journal_tree']

        self.assertEqual(
            journal_tree['subjournal'].get_report_cell(from_event='FVZ'),
            '100'
        )

    def test_get_journals_work_on_dates(self):
        """
        Модель Journal заполняет таблицу для показа статистики
        работы по всем журналам на несколько дат
        """
        journal_tree = prepare_journal_tree_records()
        res = Journal.get_journals_work_on_dates(
            root_unit=journal_tree['unit_root'],
            start_date=date(2015, 2, 16),
            days_cnt=3
        )

        self.assertEqual(
            res,
            [
                ['2015-02-16', '2015-02-17', '2015-02-18'],
                ['unit_root'], ['--subunit1', '-', '-', '-'],
                ['--subunit2', '24:00', '-', '-']
            ]
        )


class ReportModelTest(TestCase):

    def test_prepare_journals_id_for_report(self):
        """
        Модель Report готовит таблицу с номерами журналов.
        """
        journal_tree = prepare_journal_tree()
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

        ids_table = report.prepare_journals_id_for_report()['journals_id']
        self.assertEqual(
            ids_table,
            [
                [journal_tree['journal1'].id, journal_tree['journal1'].id],
                [journal_tree['journal2'].id, journal_tree['journal2'].id],
            ])

    def test_prepare_journals_id_for_report_with_subunit(self):
        """
        Модель Report готовит таблицу с номерами журналов.\
        Включаются колонки подоборудования.
        """
        journal_tree = prepare_journal_tree()
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

        ids_table = report.prepare_journals_id_for_report()['journals_id']

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
        Модель Report готовит таблицу с номерами журналов, включая подоборудование.\
        Обрабатывается отсутствие заданного подоборудования в составе одного из объектов.
        """
        journal_tree = prepare_journal_tree()
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

        ids_table = report.prepare_journals_id_for_report()['journals_id']

        self.assertEqual(
            ids_table,
            [
                [journal_tree['journal1'].id,
                 journal_tree['detail12'].journal.id],
                [journal_tree['journal2'].id,
                 None],
            ])

    def test_prepare_report_data(self):
        """
        Модель Report готовит данные отчета для вывода
        проверяется порядок вывода, формат вывода,
        правильность расчета
        """
        report = prepare_journal_tree_records_report()

        self.assertEqual(
            report.prepare_report_data(),
            [['Оборудование', 'Наработка', 'Наработка с капремонта',
              'Дата капремонта', 'Наработка detail1', 'Замена detail1', 'Наработка detail2', 'Замена detail2'],
             ['subunit1', '260', '10', '15.02.2015', '260', '-', '260', '-'],
             ['subunit2', '164', '-', '-', '34', '15.02.2015', '-', '-']]
        )

    def test_get_reports_for_select(self):
        """
        Модель Report готовит список (rep_id, rep_title) для test_reports_for_select
        """
        report = prepare_journal_tree_records_report()

        self.assertEqual(
            Report.get_reports_collection(report.equipment),
            [(report.id, 'Test Report'), ]
        )
