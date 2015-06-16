from django.test import TestCase
from django.core.urlresolvers import reverse
import datetime


from statistics.models import Journal
from catalog.models import Unit


def create_record(eq_name='Test equipment'):
    eq = Unit(name=eq_name)
    eq.save()
    journal = Journal(equipment_id=eq.id)
    journal.save()
    rec = journal.record_set.create(
        date=datetime.date.today()-datetime.timedelta(days=1),
        pusk_cnt=1,
        ostanov_cnt=1,
        work=datetime.timedelta(hours=5),
        period_length=24,)
    return rec


class JournalViewTests(TestCase):

    def test_jornal_show(self):
        '''
        Вход на страницу журнала (show) позволяет увидеть записи журнала
        '''
        rec = create_record()
        yesturday = datetime.date.today()-datetime.timedelta(days=1)
        response = self.client.get(
            reverse('statistics:show',
                    kwargs={'journal_id': rec.journal_id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, yesturday.strftime('%d.%m.%Y'))

    def test_journal_edit_form(self):
        '''
        Форма редактирования записи журнала (record_edit) показывает
        в полях формы данные объекта записи при вызове через GET
        '''
        rec = create_record()
        response = self.client.get(
            reverse('statistics:record_edit',
                    kwargs={'journal_id': rec.journal_id, 'record_id': rec.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '05:00:00')
