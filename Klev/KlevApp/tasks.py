# This is a file for the background tasks. 
# Make sure to have django-background-task 0.1.8 installed
# In order to have tasks run, run "python manage.py process_tasks"
from background_task import background
import random
import models

def start_listen_for_updates(deviceName):
	print "Starting to listen for updates to {0}".format(deviceName)
	listen_for_updates(deviceName)


@background(schedule=10) #start 20 seconds from now
def listen_for_updates(deviceName):
	print "Checking for updates to {0}".format(deviceName)
	#TODO replace this with something that talks to the node
	rand_val = random.random()
	new_state = None
	if rand_val < 0.1:
		new_state = models.ABNORMAL_STATE
	elif rand_val < 0.55:
		new_state = models.ON_STATE
	else:
		new_state = models.OFF_STATE

	print "{0} is now in the {1} state".format(deviceName, new_state)
	device = models.Device.objects.get(deviceName = deviceName)
	device.deviceState = new_state
	device.save()


	# This needs to call itself to schedule itself again
	listen_for_updates(deviceName)

	

@background(schedule=1)
def test_task():
	print "----Hello from test_task()----"

test_task()