from django.test import TestCase
from django.core.urlresolvers import reverse
# from datetime import date, timedelta

from statistics.tests import factories


class JournalViewTests(TestCase):

    def test_journal_detail_show_stat(self):
        """
        Jornal detail view show base work statistic testing
        """
        journal = factories.prepare_journal_tree()['full_journal']
        journal.set_record_data(factories.form_data())
        response = self.client.get(
            reverse('statistics:show', kwargs={'journal_id': journal.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '5:00')

    def test_journal_detail_show_ext_stat(self):
        """
        Jornal detail view show ext_state if the last exist testing
        """
        journal = factories.prepare_journal_tree()['full_journal']
        journal.set_record_data(factories.form_data())
        response = self.client.get(
            reverse('statistics:show', kwargs={'journal_id': journal.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '19:00')
