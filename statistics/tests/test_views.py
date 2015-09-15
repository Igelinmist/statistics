from django.test import TestCase
from django.core.urlresolvers import reverse

from .helpers_foo import prepare_journal_tree, form_data
from .helpers_foo import prepare_test_db_for_report


class JournalViewTests(TestCase):

    def test_journal_detail_show_stat(self):
        """
        Jornal detail view show base work statistic testing
        """
        journal = prepare_journal_tree()['full_journal']
        journal.set_record_data(form_data())
        response = self.client.get(
            reverse('statistics:show', kwargs={'journal_id': journal.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5:00')

    def test_journal_detail_show_ext_stat(self):
        """
        Jornal detail view show ext_state if the last exist testing
        """
        journal = prepare_journal_tree()['full_journal']
        journal.set_record_data(form_data())
        response = self.client.get(
            reverse('statistics:show', kwargs={'journal_id': journal.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '19:00')

    def test_reports_index_show(self):
        """
        Приложение показывает существующие отчеты
        """
        prepare_test_db_for_report()
        response = self.client.get(reverse('statistics:reports'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Report")

    def test_report_show(self):
        """
        Приложение показывает отчет
        """
        report = prepare_test_db_for_report()['report']
        response = self.client.get(reverse(
            'statistics:report',
            kwargs={'report_id': report.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Report")
        self.assertContains(response, "Наработка с ввода/замены")
