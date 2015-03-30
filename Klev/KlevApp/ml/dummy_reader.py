class DummyReader:
	def __init__(self):
		self.DATA_STRINGS = '''9.79862726656 9.98905797144 9.97196757436
9.93208390056 9.51682254847 10.4531578568
9.5485137535 10.0030981206 10.3940100046
9.94534559642 9.95891396408 9.69884758159
10.0364433067 9.65933838946 9.83632867946
9.97523460856 9.99807165765 10.4253013729
9.82326537093 10.011420212 10.2814051553
10.3407204007 10.2773097784 9.60834326349
9.56572604801 10.3727872742 9.96412956995
10.2830573296 10.1511034919 10.3249918493
10.0190261433 9.97094121727 10.3617381923
9.82794516456 10.047105428 9.61011164639
DONE'''.split("\n")

		self.CUR_LINE = 0
	def start_on_training():
		pass

	def start_off_training():
		pass

	def end_training():
		pass

	'''Real impl should read a line over 802.15.4, block until one available'''
	def read_line(self, device_id):
		result = self.DATA_STRINGS[self.CUR_LINE]
		self.CUR_LINE += 1
		if(self.CUR_LINE == len(self.DATA_STRINGS)):
			self.CUR_LINE = 0
		return result

	def end_of_msg_str():
		return "DONE"






