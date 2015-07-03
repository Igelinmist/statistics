from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    url(r'^account_show$', views.account_show, name='account_show'),
    url(r'^account_edit$', views.account_edit, name='account_edit'),
)
