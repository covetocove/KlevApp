from django.db import models

import tasks

ON_STATE = 'ON'
OFF_STATE = 'OFF'
ABNORMAL_STATE = 'ABNORMAL'

# Create your models here.
class Device(models.Model):
	deviceName = models.CharField(max_length = 42)
	make = models.CharField(max_length = 42)
	modelNum = models.CharField(max_length = 42)
	location = models.CharField(max_length = 80)
	deviceState = models.CharField(max_length = 20)
	trained = models.IntegerField(default = 0);
	photo = models.ImageField(upload_to="deviceImages", null=True, blank=True, default = None)

def extra_device_setup(sender, instance, created, *args, **kwargs):
	if created:
		print "---Performing extra setup for new device---"
		tasks.start_listen_for_updates(instance.deviceName)

from django.db.models.signals import post_save
post_save.connect(extra_device_setup, sender=Device)

#end of Device stuff

class Location(models.Model):
	name = models.CharField(max_length = 50)
	address = models.CharField(max_length = 80)

	def __str__(self):
		return "%s, at %s" % self.name, self.address

