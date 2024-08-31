from .utils import *


def generate_input(spec):
	result = []
	for item in spec:
		try:
			item_type = item['type']
			if item_type == 'int':
				limit = [resolve_reference(l, result) for l in item['limit']]
				result.append(generate_int(limit))
			elif item_type == 'float':
				limit = [resolve_reference(l, result) for l in item['limit']]
				precision = item.get('precision', 2)
				result.append(generate_float(limit, precision))
			elif item_type == 'string':
				length = resolve_reference(item['length'], result)
				char_set = item.get('char_set', string.ascii_lowercase)
				result.append(generate_string(length, char_set))
			elif item_type == 'array':
				size = resolve_reference(item['size'], result)
				gen_func = globals()[f"generate_{item['element_type']}"]
				limit = [resolve_reference(l, result) for l in item['limit']]
				result.append(generate_array(size, gen_func, limit))
			elif item_type == '2d_array':
				rows = resolve_reference(item['rows'], result)
				cols = resolve_reference(item['cols'], result)
				gen_func = globals()[f"generate_{item['element_type']}"]
				limit = [resolve_reference(l, result) for l in item['limit']]
				result.append(generate_2d_array(rows, cols, gen_func, limit))
			elif item_type == 'newline':
				result.append('\n')
			else:
				raise ValueError(f"Unknown type: {item_type}")
		except KeyError as e:
			raise KeyError(f"Missing key in spec: {e}")
		except Exception as e:
			raise Exception(f"Error generating input for {item_type}: {e}")
	return result


def generate_output_string(input_data, spec):
	output = []
	for item, data in zip(spec, input_data):
		if item['type'] == 'newline':
			output.append('\n')
		elif item['type'] in ['int', 'float', 'string']:
			output.append(str(data))
		elif item['type'] == 'array':
			output.append(' '.join(map(str, data)))
		elif item['type'] == '2d_array':
			for row in data:
				output.append(' '.join(map(str, row)))
				output.append('\n')
	return '\n'.join(line.strip() for line in ' '.join(output).split('\n')).strip() + '\n'



