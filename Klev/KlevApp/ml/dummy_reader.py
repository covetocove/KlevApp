
from generate_sample import generate_sample_data

class DummyReader:

	ON = 'on'
	OFF = 'off'

	pos_center = (1,2,3,4,5,6)
	neg_center = (6,5,4,3,2,1)

	pos_noise = 0.5
	neg_noise = 0.5

	num_pos_examples = 100
	num_neg_examples = 100

	def __init__(self):
		self.state = None
		self.data = None
		self.examples_read = 0


	def start_on_training(self, device_id):
		self.state = DummyReader.ON
		self.examples_read = 0
		self.data = generate_sample_data(self.pos_center, 
											self.neg_center,
											self.pos_noise,
											self.neg_noise,
											self.num_pos_examples,
											0) #no negative (off) examples
		

	def start_off_training(self, device_id):
		self.state = DummyReader.OFF
		self.examples_read = 0
		self.data = self.pos_data = generate_sample_data(self.pos_center, 
											self.neg_center,
											self.pos_noise,
											self.neg_noise,
											0,
											self.num_neg_examples) #no negative (off) examples

	def end_training(self, device_id):
		pass

	'''Real impl should read a line over 802.15.4, block until one available'''
	def read_line(self, device_id):
		if self.state is None:
			print "[DummyReader#read_line()] Trying to read while in None state"
			return None

		if(self.examples_read == len(self.data)):
			return self.end_of_msg_str()
		else:
			example = self.data[self.examples_read]
			self.examples_read += 1
			return " ".join(map(str, example.features))
		

	def end_of_msg_str(self):
		return "DONE"






