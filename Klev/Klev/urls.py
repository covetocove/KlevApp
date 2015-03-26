from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Klev.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^klev/', include('KlevApp.urls')),
) 