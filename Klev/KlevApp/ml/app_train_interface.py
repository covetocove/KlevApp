data_and_files_dir = "data_and_models"

import dummy_reader
import train

def get_data_file_name(device_id):
	return "KlevApp/ml/data_and_models/data_{0}".format(device_id)

#
def convert_line_to_libsvm_example(is_positive, feature_string):
	feature_str_arr = feature_string.split(' ')
	features = [float(feature_str) for feature_str in feature_str_arr]
	label = '+1'
	if not is_positive:
		label = '-1'
	result_str_list = [label]
	for i in xrange(len(features)):
		result_str_list.append(" {0}:{1}".format(i+1, features[i]))
	return ''.join(result_str_list)

def train_state(device_id, is_on):

	data_file_name = get_data_file_name(device_id)
	data_file = None
	# User trains "off" first, so we want to overwrite
	# the file if it already exists when we write the
	# "off" data
	if is_on:
		data_file = open(data_file_name, 'a')
	else:
		data_file = open(data_file_name, 'w')
	try:
		reader = dummy_reader.DummyReader()
		if is_on:
			reader.start_on_training(device_id)
		else:
			reader.start_off_training(device_id)
		line = reader.read_line(device_id)
		while(line.strip() != reader.end_of_msg_str() and len(line) > 0):
			to_write = convert_line_to_libsvm_example(is_on, line) + '\n'
			data_file.write(to_write)
			line = reader.read_line(device_id)
		if is_on:
			data_file.close()
			train.scale_and_train(data_file_name)
	finally:
		if data_file is not None:
			data_file.close()

