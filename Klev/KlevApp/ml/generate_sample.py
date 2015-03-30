import random

class Example:
	def __init__(self, label, features):
		self.label = label
		self.features = features

	def __str__(self):
		res = "{0:+}".format(self.label)
		for i in xrange(len(self.features)):
			res += " {0}:{1}".format(i+1, self.features[i])
		return res

	def to_str_no_label(self):
		res = ""
		for i in xrange(len(self.features)):
			res += " {0}:{1}".format(i+1, self.features[i])
		return res


# Generates sample data where positive examples are within error_pos of
# center_pos and negative examples are within error_neg of center_neg.
# Returns a list Examples
def generate_sample_data(center_pos, center_neg, error_pos, error_neg, num_pos, num_neg):
	random.seed()
	if(len(center_pos) != len(center_neg)):
		print ("Mis-match between length of center_pos (#{0}), and center_neg (#{1})" 
			 .format(len(center_pos), len(center_neg)))
		return None
	data = []
	for i in xrange(num_pos):
		features = [(val - error_pos + 2*error_pos*random.random()) \
			for val in center_pos]
		data.append(Example(1, features))
	for i in xrange(num_neg):
		features = [(val - error_neg + 2*error_neg*random.random()) \
			for val in center_neg]
		data.append(Example(-1, features))
	return data


def write_data(output_file_name, data, include_label=True):
	output_file = open(output_file_name, 'w')
	try:
		for example in data:
			if(include_label):
				output_file.write(str(example) + "\n")
			else:
				output_file.write(example.to_str_no_label() + "\n")
	finally:
		output_file.close()


def main():
	center_pos = [10,10,10]
	center_neg = [0,0,0]
	#center_pos = [4, 8, 15, 16, 23, 42]
	#center_neg = [-4, -20, -21, -23, -26, -35]
	error_pos = 0.5
	error_neg = 1.0
	num_pos= 50
	num_neg = 50
	output_file_name = "data/sample"

	data = generate_sample_data(center_pos, center_neg, error_pos, error_neg, num_pos, num_neg)
	write_data(output_file_name, data, include_label=True)



if __name__ == "__main__":
	main()