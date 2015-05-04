

import serial
import time

MSG_START = "#"
DELIMITER_SEQ = "|"
DATA_DIR_PATH = ""

tids_processed = set()
cur_req_id = 1

ser = serial.Serial(4, 57600, timeout=15)

class serial_message(object):
	def __init__(self, tid, nid, state):
		"""transmission id, node id, node state"""
		self.tid = tid
		self.nid = nid
		self.state = state

def get_serial_line():
	# TRANSMISSION_ID - NODE_ID - STATE
	return serial_message(1, 1, "ON")
	
def send_serial_ack(tid):
	return
'''
def send_serial_req(rid, nid):
	message = str(rid) + DELIMITER_SEQ + str(nid) + chr(0) #end with null
	return
'''

def get_data():
	send_req_and_get_resp("GET_DATA")

def send_two_class_model():
	send_file("SENDING_TWO_CLASS_MODEL", "KlevApp/ml/data_and_models\data_dummy_sample.model")

def send_one_class_model():
	send_file("SENDING_ONE_CLASS_MODEL", "KlevApp/ml/data_and_models\data_dummy_sample.one_class_model")

def send_scaling_params():
	send_file("SENDING_SCALING_PARAMS", "KlevApp/ml/data_and_models\data_dummy_sample.send_scaling_params")

def send_file(header, file_name):
	send_req_and_get_resp(header)
	model_file = open(file_name)
	for line in model_file:
		send_req_and_get_resp(line[:-1] + "\r\n\0x00")
	model_file.close()

def send_req_and_get_resp(msg_body):
	global cur_req_id
	global ser
	message = MSG_START + str(cur_req_id) +  DELIMITER_SEQ + msg_body + "\r\n\x00"
	ser.write(message)
	print "--> " + message
	cur_req_id += 1
	ser.flush()
	ser.readline() #need this to flush what we just sent?
	print "<-- "+  ser.readline()
	return


# requests an update on the state of node_id node
def update_data(node_id):
	this_req_id = cur_req_id
	cur_req_id += 1

	while (serial_input == None):
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
		else:
			print serial_input

	tids_processed.add(serial_input.tid)

	file_path = DATA_DIR_PATH + str(serial_input.tid)
		
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	file_line = str(serial_input.nid) + DELIMITER_SEQ + timestamp + \
				DELIMITER_SEQ + str(serial_input.state) + "\n"

	with open(file_path, "a") as f:
		f.write(file_line)

	send_serial_ack(serial_input.tid)


"""
ser = serial.Serial('USB\\VID_2341&PID_0043\\952383432343510162A0',9600,timeout=1)

ser.flushInput()
ser.flushOutput()

while (1):
	print "Testing..."
	data_row = ser.readline()
	print data_row

"""