

import serial
import time

MSG_START = "#"
DELIMITER_SEQ = "|"
DATA_DIR_PATH = ""
MSG_END = "\x00"
LINE_END = "\r\n" + MSG_END

ACK = "ACK"
MAX_LINE_LEN = 32

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
	send_file("SENDING_TWO_CLASS_MODEL", "KlevApp/ml/data_and_models\data_toaster.model")

def send_one_class_model():
	send_file("SENDING_ONE_CLASS_MODEL", "KlevApp/ml/data_and_models\data_dummy_sample.one_class_model")

def send_scaling_params():
	send_file("SENDING_SCALING_PARAMS", "KlevApp/ml/data_and_models\data_dummy_sample.send_scaling_params")

def send_file(header, file_name):
	send_req_and_get_resp(header)
	model_file = open(file_name)
	for line in model_file:
		if(len(line) > MAX_LINE_LEN):
			i = 0
			end_ind = i + MAX_LINE_LEN
			#we need to make sure not to send an empty line as the message
			#Check if we can send the rest in < 2 messages
			while(end_ind + MAX_LINE_LEN < len(line)):
				send_req_wait_ack(line[i:end_ind] + MSG_END)		
				i += MAX_LINE_LEN
				end_ind = i + MAX_LINE_LEN
			# Always send the max amount in the last message, so it
			# can't be empty
			# Send however much needed in the second to last to accomplish that
			end_ind = len(line) - MAX_LINE_LEN
			send_req_wait_ack(line[i:end_ind] + MSG_END)
			i = end_ind
			end_ind = len(line)
			send_req_wait_ack(line[i:end_ind] + MSG_END)

		else:
			send_req_wait_ack(line[:-1] + LINE_END)
		send_req_wait_ack(LINE_END)
	model_file.close()

def send_req(msg_body):
	global cur_req_id
	global ser
	message = MSG_START + str(cur_req_id) +  DELIMITER_SEQ + msg_body + LINE_END
	ser.write(message)
	print "--> " + message
	cur_req_id += 1
	ser.flush()

def send_req_wait_ack(msg_body):
	send_req(msg_body)
	read_line = ser.readline()
	while read_line.find(ACK) < 0:
		print "(ignoring {0})".format(read_line)
		read_line = ser.readline()
	print "<-- " + read_line

def send_req_and_get_resp(msg_body):
	send_req(msg_body)
	read_line = ser.readline() #need this to flush what we just sent?
	if read_line.find("Hello") > 0:
		print "Tossing {0}".format(read_line)
		read_line = ser.readline()

	print "(first read {0})".format(read_line)
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