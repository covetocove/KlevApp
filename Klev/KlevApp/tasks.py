# This is a file for the background tasks. 
# Make sure to have django-background-task 0.1.8 installed
# In order to have tasks run, run "python manage.py process_tasks"
from background_task import background
import random
import models
import time

ON_STATE_STR = "STATE_ON"
OFF_STATE_STR = "STATE_OFF"
ABN_STATE_STR = "STATE_ABNORMAL"
DELIMITER_SEQ = "---"
DATA_DIR_PATH = ""

GET_STATE_STR = "GET_STATE"

#send this when we want training data, followed by a line with the number of data points (rows)  wanted
GET_DATA_STR = "GET_DATA" 

# When training, the node expects the two-class model string,
# then the scaling parameters,
# then the 1-class model to be sent
# The end of each of those should be marked by an empty line (with \r),
# i.e. the last 4 characters sent should be \r\n\r\n
# Transaction should look like
# send "SENDING_MODEL\r\n"
# send two-class model string
# send "\r\n"
# send scaling-info
# send "\r\n"
# send one-class model string
# send "\r\n"
SENDING_MODEL = "SENDING_MODEL"

def start_listen_for_updates(deviceName, nodeid):
	print "Starting to listen for updates to {0}".format(deviceName)
	listen_for_updates(deviceName, nodeid)

class serial_message(object):
	def __init__(self, tid, nid, state):
		"""transmission id, node id, node state"""
		self.tid = tid
		self.nid = nid
		self.state = state

def get_serial_line(tid = [1]):
	# TRANSMISSION_ID - NODE_ID - STATE
	# janky way to increment the transmission id each time
	this_tid = tid[0]
	tid[0] += 1

	print "tid = " + str(tid[0])

	rand_val = random.random()
	new_state = None
	if rand_val < 0.1:
		new_state = ABN_STATE_STR
	elif rand_val < 0.55:
		new_state = ON_STATE_STR
	else:
		new_state = OFF_STATE_STR

	print "new_state = " + new_state

	return serial_message(this_tid, 1, new_state)
	
def send_serial_ack(tid):
	return

def send_serial_req(rid, nid):
	message = str(rid) + DELIMITER_SEQ + str(nid)
	return

# requests an update on the state of node_id node
def update_data(node_id, cur_req_id = [1], tids_processed = set()):
	print "in update_data\n"

	# janky way to increment the request id each time
	this_req_id = cur_req_id[0]
	cur_req_id[0] += 1
	print "this_req_id = " + str(this_req_id)

	serial_input = None
	while (serial_input == None):
		print "looping on serial input"
		send_serial_req(this_req_id, node_id)
		time.sleep(0.25)
		serial_input = get_serial_line()
		if (serial_input == None):
			continue
		if (serial_input.tid in tids_processed):
			print "Repeated message"
			send_serial_ack(serial_input.tid)
			serial_input = None
		elif (serial_input.nid != node_id):
			print "Different node id received"
			serial_input = None

	tids_processed.add(serial_input.tid)

	file_path = DATA_DIR_PATH + str(node_id)
		
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	file_line = str(serial_input.nid) + DELIMITER_SEQ + timestamp + \
				DELIMITER_SEQ + str(serial_input.state) + "\n"

	with open(file_path, "a") as f:
		f.write(file_line)

	send_serial_ack(serial_input.tid)

	return serial_input.state

@background(schedule=10) #start 20 seconds from now
def listen_for_updates(deviceName, nodeid):
	print "Checking for updates to {0}".format(deviceName)

	new_state_str = update_data(nodeid)
	if (new_state_str == ON_STATE_STR):
		new_state = models.ON_STATE
	elif (new_state_str == OFF_STATE_STR):
		new_state = models.OFF_STATE
	elif (new_state_str == ABN_STATE_STR):
		new_state = models.ABNORMAL_STATE
	else:
		print "ERROR: Invalid state received!\n"
		new_state = models.ABNORMAL_STATE

	device = models.Device.objects.get(nodeid = nodeid, deviceName = deviceName)
	device.deviceState = new_state
	device.save()

	# This needs to call itself to schedule itself again
	listen_for_updates(deviceName, nodeid)

	

@background(schedule=1)
def test_task():
	print "----Hello from test_task()----"