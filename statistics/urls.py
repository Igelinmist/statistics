from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<journal_id>[0-9]+)/$', views.show, name='show'),
    url(r'^(?P<journal_id>\d+)/new_record$',
        views.new_record,
        name='new_record'),
]
