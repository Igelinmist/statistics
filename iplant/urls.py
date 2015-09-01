from django.conf.urls.static import static
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

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

# В конце файла:

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True
urlpatterns += staticfiles_urlpatterns()
