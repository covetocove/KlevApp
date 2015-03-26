from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'KlevApp.views.index', name='index'),
    url(r'^addDevice/', 'KlevApp.views.addDevice', name='addDevice'),
    url(r'^devices/', 'KlevApp.views.devices', name='devices'),
	url(r'^deviceAdded/$', 'KlevApp.views.deviceAdded', name='deviceAdded'),


)