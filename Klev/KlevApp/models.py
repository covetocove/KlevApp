from django.db import models

# Create your models here.
class Device(models.Model):
	deviceName = models.CharField(max_length = 42)
	make = models.CharField(max_length = 42)
	modelNum = models.CharField(max_length = 42)
	location = models.CharField(max_length = 80)
	deviceState = models.CharField(max_length = 20)
	trained = models.IntegerField(default = 0);
	photo = models.ImageField(upload_to="deviceImages", null=True, blank=True, default = None)


class Location(models.Model):
	name = models.CharField(max_length = 50)
	address = models.CharField(max_length = 80)

	def __str__(self):
		return "%s, at %s" % self.name, self.address

