from django import forms
import datetime

from .models import PERIOD_IN_CHOICES


class RecordForm(forms.Form):
    rec_date = forms.DateField(
        initial=str(datetime.date.today() - datetime.timedelta(days=1)),
        label='Дата')
    rec_period = forms.ChoiceField(
        choices=PERIOD_IN_CHOICES,
        label='Период')
    work = forms.CharField(
        initial='00:00',
        max_length=7,
        label='Работа')
    reserv = forms.CharField(
        initial='00:00', max_length=7,
        label='Резерв')
    av_rem = forms.CharField(
        initial='00:00', max_length=7,
        label='Аварийный ремонт')
    tek_rem = forms.CharField(
        initial='00:00',
        max_length=7,
        label='Текущий ремонт')
    kap_rem = forms.CharField(
        initial='00:00',
        max_length=7,
        label='Капитальный ремонт')
    sr_rem = forms.CharField(
        initial='00:00',
        max_length=7,
        label='Средний ремонт')
    reconstr = forms.CharField(
        initial='00:00',
        max_length=7,
        label='Реконструкция')
    starts = forms.IntegerField(initial=0, label='Кол-во пусков')
    stops = forms.IntegerField(initial=0, label='Кол-во остановов')
