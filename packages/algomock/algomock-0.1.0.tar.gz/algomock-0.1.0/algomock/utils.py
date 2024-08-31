import random
import string


def generate_int(limit):
	return random.randint(limit[0], limit[1])


def generate_float(limit, precision=2):
	return round(random.uniform(limit[0], limit[1]), precision)


def generate_string(length, char_set=string.ascii_lowercase):
	return ''.join(random.choice(char_set) for _ in range(length))


def generate_array(size, gen_func, limit):
	return [gen_func(limit) for _ in range(size)]


def generate_2d_array(rows, cols, gen_func, limit):
	return [[gen_func(limit) for _ in range(cols)] for _ in range(rows)]


def resolve_reference(value, generated_values):
	if isinstance(value, str) and value.startswith('$'):
		index = int(value[1:])
		return generated_values[index]
	return value
