from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^statistics/', include('statistics.urls', namespace="statistics")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += patterns(
    'django.contrib.auth.views',

    url(r'^login/$', 'login', {'template_name': 'accounts/login.html'}, name='iplant_login'),
    url(r'^logout/$', 'logout', name='iplant_logout'),
)
