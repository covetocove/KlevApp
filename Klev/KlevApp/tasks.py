# This is a file for the background tasks.
# Make sure to have django-background-task 0.1.8 installed
# In order to have tasks run, run "python manage.py process_tasks"
from background_task import background
import random
import models
import time
import mutex

ON_STATE_STR = "STATE_ON"
OFF_STATE_STR = "STATE_OFF"
ABN_STATE_STR = "STATE_ABNORMAL"
START_CHAR = "#" #used to mark start of message. Can appear multiple times at start
MESSAGE_NUM_END_CHAR = "|"
DATA_DIR_PATH = ""
GET_STATE_STR = "GET_STATE"
DELIMITER_SEQ = "---"

# For all messages the Hub will send them until it gets
# a message back from the node with a matching transaction number
# The node will send messages until it gets a message from the Hub
# with a transaction number one greater than the last seen

# Sample message from HUB
# ###42|GET_DATA\r\n
# ^^^^This message means that this is the 42nd transaction,
# the node should start sending data.
# The message the node sends back should start with ###42|
# For sending the model, the hun should send:
# ###51|SENDING_TWO_CLASS_MODEL\r\n
# For this line, and each following one, the node
# should send something back that looks like
# ###51|ACK\r\n
# The hub will send lines that start with ###<transaction number>|
# followed by the line from the model file being sent


ACK = "ACK"

def start_listen_for_updates(deviceName, nodeid):
	print "Starting to listen for updates to {0}".format(deviceName)
	listen_for_updates(deviceName, nodeid)

class serial_message(object):
	def __init__(self, tid, nid, state):
		"""transmission id, node id, node state"""
		self.tid = tid
		self.nid = nid
		self.state = state

def get_serial_state_line(tid = [1]):
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

def send_serial_state_ack(tid):
        message = ACK + str(tid) + "\r\n"
	return

def send_serial_state_req(rid, nid):
	message = GET_STATE_STR + str(rid) + DELIMITER_SEQ + str(nid) + "\r\n"
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
		send_serial_state_req(this_req_id, node_id)
		time.sleep(0.25)
		serial_input = get_serial_state_line()
		if (serial_input == None):
			continue
		if (serial_input.tid in tids_processed):
			print "Repeated message"
			send_serial_state_ack(serial_input.tid)
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

	send_serial_state_ack(serial_input.tid)

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

	device = models.Device.objects.get(nodeid = nodeid,
                                           deviceName = deviceName)


        print device.deviceName + ": nodeid=" + str(device.nodeid) + \
            ";Old device state: " + str(device.deviceState)


	device.deviceState = new_state
	device.save()

	# This needs to call itself to schedule itself again
	listen_for_updates(deviceName, nodeid)



@background(schedule=1)
def test_task():
	print "----Hello from test_task()----"
