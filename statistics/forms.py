from bootstrap3_datetime.widgets import DateTimePicker

from django import forms
from datetime import timedelta, date

from .models.journal import EVENT_CHOICES


class RecordForm(forms.Form):
    date = forms.DateField(
        initial=date.today()-timedelta(days=1),
        label='Дата')
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


class EventForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "startDate": "01.01.1945",
                                       "pickTime": False}),
        label='Дата события:',
    )
    event = forms.ChoiceField(
        choices=EVENT_CHOICES,
        label='Событие',
    )


class ChooseDateForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": False}),
        label='На дату:',
    )


class ChooseReportForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={"locale": "ru",
                                       "pickTime": False}),
        label='На дату:',
    )

    def __init__(self, choices=None, *args, **kwargs):
        super(ChooseReportForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields.update(
                {'report_id': forms.ChoiceField(widget=forms.Select,
                                                label='отчет:',
                                                choices=choices)}
            )
