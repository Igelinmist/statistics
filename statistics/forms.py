from django import forms
from datetime import timedelta, date

from .models import PERIOD_IN_CHOICES


class RecordForm(forms.Form):
    date = forms.DateField(
        initial=date.today()-timedelta(days=1),
        label='Дата')
    period_length = forms.ChoiceField(
        choices=PERIOD_IN_CHOICES,
        label='Период')
    work = forms.DurationField(
        initial='00:00:00',
        label='Работа')
    rsv = forms.DurationField(
        initial='00:00:00',
        label='Резерв',
        required=False)
    arm = forms.DurationField(
        initial='00:00:00',
        label='Аварийный ремонт',
        required=False)
    trm = forms.DurationField(
        initial='00:00:00',
        label='Текущий ремонт',
        required=False)
    krm = forms.DurationField(
        initial='00:00:00',
        label='Капитальный ремонт',
        required=False)
    srm = forms.DurationField(
        initial='00:00:00',
        label='Средний ремонт',
        required=False)
    rcd = forms.DurationField(
        initial='00:00:00',
        label='Реконструкция',
        required=False)
    pusk_cnt = forms.IntegerField(
        initial=0,
        label='Пусков')
    ostanov_cnt = forms.IntegerField(
        initial=0,
        label='Остановов')

    def init_form(self, record=None, ext_statistic=None):
        if ext_statistic:
            if record:
                for state_item in record.stateitem_set.all():
                    self.fields[state_item.state.lower()].initial = state_item.time_in_state
        else:
            for state_item in ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
                self.fields[state_item].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(RecordForm, self).clean()
        setting_time = timedelta(hours=int(cleaned_data.get('period_length')))
        common_time = timedelta(hours=0)
        for name in ('work', 'rsv', 'trm', 'arm', 'krm', 'srm', 'rcd'):
            common_time += cleaned_data.get(name)
        if setting_time != common_time:
            raise forms.ValidationError(
                'Длительность периода не сходится с суммой времен состояний!')
