import unittest

def is_alphabetized(input1, opr, input2, exp_out):
	if opr == '+':
		if input1 + input2 > exp_out:
			# LOGGER.info("True")
			return True
		else:
			return False

	if opr == '*':
		if input1 * input2 == exp_out:
			# LOGGER.info("True")
			return True
		else:
			return False

	if opr == '/':
		if input1/input2 == exp_out:
			# LOGGER.info("True")
			return True
		else:
			return False

	if opr == '-':
		if input1 - input2 == exp_out:
			# LOGGER.info("True")
			return True
		else:
			return False

def make_method(input1, opr, input2, exp_out):
	
	def test_input(self):
		self.assertTrue(is_alphabetized(input1, opr, input2, exp_out), u'{} {} {} != {} was not considered alphabetized'.format(input1, opr, input2, exp_out))

	test_input.__name__ = 'test_alphabetical_{}_{}_{}_{}'.format(input1, opr, input2, exp_out)
	return test_input


def add_methods(inputs):
	"""
	Take a TestCase and add a test method for each input
	"""
	def decorator(klass):
		for inps in inputs:
			test_input = make_method(inps[0], inps[1], inps[2], inps[3])
			setattr(klass, test_input.__name__, test_input)
		return klass

	return decorator

def get_inputs():
	# inp = [[''], ['a'], ['aaaaa'], ['ab'], ['abcd'], ['A-Cert'], ['iOS']]
	inp = [[3, '+', 5, 8], [10, '-', 5, 5], [5, '*', 5, 25], [100, '/', 10, 10]]
	return inp

@add_methods(get_inputs())
class IsAlphabetizedTestCase(unittest.TestCase):
	pass
