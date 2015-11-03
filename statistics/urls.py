from django.conf.urls import url

from statistics.views import journals_view
from statistics.views import records_view
from statistics.views import events_view
from statistics.views import reports_view

urlpatterns = [
    url(r'^$',
        journals_view.index,
        name='index'),
    url(r'^journals_on_date$',
        journals_view.journals_on_date,
        name='journals_on_date'),
    url(r'^journals_write$',
        journals_view.journals_write,
        name='journals_write'),
    url(r'^(?P<journal_id>[0-9]+)/$', journals_view.show, name='show'),
    url(r'^(?P<journal_id>[0-9]+)/records$',
        records_view.records,
        name='records'),
    url(r'^(?P<journal_id>\d+)/simple_record_new$',
        records_view.simple_record_create,
        name='simple_record_new'),
    url(r'^(?P<journal_id>\d+)/record_new$',
        records_view.record_create,
        name='record_new'),
    url(r'^(?P<journal_id>\d+)/record_edit/(?P<record_id>\d+)$',
        records_view.record_update,
        name='record_edit'),
    url(r'^(?P<journal_id>\d+)/record_delete/(?P<record_id>\d+)$',
        records_view.record_delete,
        name='record_delete'),
    url(r'^(?P<journal_id>\d+)/event_new$',
        events_view.event_create,
        name='event_new'),
    url(r'^(?P<journal_id>\d+)/event_delete/(?P<event_id>\d+)$',
        events_view.event_delete,
        name='event_delete'),
    url(r'^reports/$',
        reports_view.reports,
        name='reports'),
    url(r'^reports/viewreport$',
        reports_view.report_show,
        name='report_show'),
]
