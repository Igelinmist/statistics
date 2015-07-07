from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$', views.show, name='show'),
    url(r'^(?P<journal_id>[0-9]+)/records$', views.records, name='records'),
    url(r'^(?P<journal_id>\d+)/record_new$',
        views.record_create,
        name='record_new'),
    url(r'^(?P<journal_id>\d+)/record_edit/(?P<record_id>\d+)$',
        views.record_update,
        name='record_edit'),
    url(r'^(?P<journal_id>\d+)/record_delete/(?P<record_id>\d+)$',
        views.record_delete,
        name='record_delete'),
    url(r'^(?P<journal_id>\d+)/event_new$',
        views.event_create,
        name='event_new'),
    url(r'^(?P<journal_id>\d+)/event_delete/(?P<event_id>\d+)$',
        views.event_delete,
        name='event_delete'),
]
