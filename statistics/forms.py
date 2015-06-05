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
        label='Работа')
    rsv = forms.DurationField(
        label='Резерв',
        required=False)
    arm = forms.DurationField(
        label='Аварийный ремонт',
        required=False)
    trm = forms.DurationField(
        label='Текущий ремонт',
        required=False)
    krm = forms.DurationField(
        label='Капитальный ремонт',
        required=False)
    srm = forms.DurationField(
        label='Средний ремонт',
        required=False)
    rcd = forms.DurationField(
        label='Реконструкция',
        required=False)
    pusk_cnt = forms.IntegerField(
        initial=0,
        label='Пусков')
    ostanov_cnt = forms.IntegerField(
        initial=0,
        label='Остановов')

    def __init__(self, *args, **kwargs):
        journal = kwargs.pop('journal', None)
        super(RecordForm, self).__init__(*args, **kwargs)
        for state_name in ('work', 'rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
            self.fields[state_name].initial = timedelta(hours=0)
        if not journal.extended_stat:
            for state_name in ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
                self.fields[state_name].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(RecordForm, self).clean()
        setting_time = timedelta(hours=int(cleaned_data.get('period_length')))
        common_time = timedelta(hours=0)
        flExt = False
        for name in ('work', 'rsv', 'trm', 'arm', 'krm', 'srm', 'rcd'):
            flExt += bool(cleaned_data.get(name))
            if cleaned_data.get(name):
                common_time += cleaned_data.get(name)
        if flExt and setting_time != common_time:
            raise forms.ValidationError(
                'Длительность периода не сходится с суммой времен состояний!')
