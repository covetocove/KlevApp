# This is a file for the background tasks. 
# Make sure to have django-background-task 0.1.8 installed
# In order to have tasks run, run "python manage.py process_tasks"
from background_task import background

def start_listen_for_updates(device):
	listen_for_updates(device)


@background(schedule=20) #start 20 seconds from now
def listen_for_updates(deviceName):
	print "TODO implement listen_for_updates"
	print deviceName

	# This needs to call itself to schedule itself again
	listen_for_updates(deviceName)

	

@background(schedule=1)
def test_task():
	print "----Hello from test_task()----"

test_task()