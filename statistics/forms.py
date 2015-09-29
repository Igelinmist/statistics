from bootstrap3_datetime.widgets import DateTimePicker

from django import forms
from datetime import timedelta

from .models.journal import EVENT_CHOICES, stat_timedelta


class RecordForm(forms.Form):
    date = forms.DateField(
        widget=DateTimePicker(options={
            "startDate": "01.01.1945",
            "pickTime": False,
        }),
        label='Дата:',
    )
    work = forms.CharField()
    rsv = forms.CharField(required=False)
    arm = forms.CharField(required=False)
    trm = forms.CharField(required=False)
    krm = forms.CharField(required=False)
    srm = forms.CharField(required=False)
    rcd = forms.CharField(required=False)
    pusk_cnt = forms.IntegerField(
        initial=0,
        min_value=0)
    ostanov_cnt = forms.IntegerField(
        initial=0,
        min_value=0)

    def __init__(self, *args, **kwargs):
        extended_stat = kwargs.pop('extended_stat', None)
        super(RecordForm, self).__init__(*args, **kwargs)
        for state_name in ('work', 'rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
            self.fields[state_name].initial = stat_timedelta(timedelta(hours=0))
        # Если в журнале нет расширенной статистики удалить из формы лишние поля
        if not extended_stat:
            for state_name in ('rsv', 'arm', 'trm', 'krm', 'srm', 'rcd'):
                self.fields.pop(state_name)


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
