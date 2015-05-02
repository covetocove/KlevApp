from django.conf.urls import patterns, include, url
from django.db import models
from tasks import start_listen_for_updates


urlpatterns = patterns('',
    url(r'^$', 'KlevApp.views.Index', name='index'),
    url(r'^addDevice/', 'KlevApp.views.AddDevice', name='addDevice'),
    url(r'^devices/', 'KlevApp.views.Devices', name='devices'),
	url(r'^deviceAdded/$', 'KlevApp.views.DeviceAdded', name='deviceAdded'),
	url(r'^trainDevice/$', 'KlevApp.views.TrainDevice', name='trainDevice'),
	url(r'^trainOff/$', 'KlevApp.views.TrainOff', name='trainOff'),
	url(r'^finishOff/$', 'KlevApp.views.FinishOff', name='finishOff'),
	url(r'^trainOn/$', 'KlevApp.views.TrainOn', name='trainOn'),
	url(r'^finishOn/$', 'KlevApp.views.FinishOn', name='finishOn'),
	url(r'^trainingFinished/$', 'KlevApp.views.TrainingFinished', name='trainingFinished'),
)

