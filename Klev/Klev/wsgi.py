"""
WSGI config for Klev project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Klev.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#This is a bit of a hack to get this to run once on startup
def setup_tasks():
	from KlevApp.models import Device
	from KlevApp.tasks import start_listen_for_updates
	devices = Device.objects.all()
	print "---Setting up for {0} devices---".format(len(devices))
	for device in devices:
		start_listen_for_updates(device.deviceName)
		
setup_tasks()