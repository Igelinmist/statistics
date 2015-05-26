from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$', views.show, name='show'),
    url(r'^(?P<journal_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<journal_id>[0-9]+)/create/$', views.create, name='create'),
    url(r'^(?P<journal_id>\d+)/new$', views.record_create, name='record_new'),
    url(r'^(?P<journal_id>\d+)/record$', views.get_record, name='record'),
]
