from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    url(r'^profile_show$', views.home, name='profile_show'),
    url(r'^profile_edit$', views.home, name='profile_edit'),
)
