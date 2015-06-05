from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$', views.show, name='show'),
    url(r'^(?P<journal_id>\d+)/record_new$',
        views.record_create_or_edit,
        name='record_new'),
    url(r'^(?P<journal_id>\d+)/record_delete/(?P<record_id>\d+)$',
        views.record_delete,
        name='record_delete'),
    url(r'^(?P<journal_id>\d+)/record_edit/(?P<record_id>\d+)$',
        views.record_create_or_edit,
        name='record_edit'),
]
