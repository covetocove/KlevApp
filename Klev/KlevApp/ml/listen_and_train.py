def convert_line(space_separated_features):
	pass

def main():
	'''Should do the following:
		1) Read a line 
		2) convert it to what lib SVM expects
		3) write it to a file
		4) train using that file as input
		5) call db_writer'''
	
	reader = DummyReader()
	while(reader.read_line() != reader.end_of_msg_str)


main()