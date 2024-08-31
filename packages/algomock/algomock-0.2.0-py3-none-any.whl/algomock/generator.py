from typing import List, Dict, Any, Callable
from .utils import (
	resolve_variable, save_variable, generate_random_int,
	generate_random_string, generate_random_array, generate_random_2d_array
)


class InputGenerator:
	def __init__(self):
		self.variables = {}
		self.type_handlers: Dict[str, Callable] = {
			'int': self.generate_int,
			'newline': self.generate_newline,
			'space': self.generate_space,
			'array': self.generate_array,
			'2d_array': self.generate_2d_array,
			'string': self.generate_string,
			'repeat_char': self.repeat_char,
			'repeat_type': self.repeat_type,
			'loop': self.process_loop,
		}

	def generate_int(self, item: Dict[str, Any], var_name: str = None) -> str:
		min_val, max_val = map(lambda x: resolve_variable(x, self.variables), item['limit'])
		value = generate_random_int(min_val, max_val)
		save_variable(var_name, value, self.variables)
		return str(value)

	def generate_array(self, item: Dict[str, Any], var_name: str = None) -> str:
		size = resolve_variable(item['size'], self.variables)
		min_val, max_val = map(lambda x: resolve_variable(x, self.variables), item['limit'])
		array = generate_random_array(size, min_val, max_val)
		save_variable(var_name, array, self.variables)
		return ' '.join(map(str, array))

	def generate_2d_array(self, item: Dict[str, Any], var_name: str = None) -> str:
		rows = resolve_variable(item['rows'], self.variables)
		cols = resolve_variable(item['cols'], self.variables)
		min_val, max_val = map(lambda x: resolve_variable(x, self.variables), item['limit'])
		array_2d = generate_random_2d_array(rows, cols, min_val, max_val)
		save_variable(var_name, array_2d, self.variables)
		return '\n'.join(' '.join(map(str, row)) for row in array_2d)

	def generate_string(self, item: Dict[str, Any], var_name: str = None) -> str:
		length = resolve_variable(item['length'], self.variables)
		value = generate_random_string(length)
		save_variable(var_name, value, self.variables)
		return value

	def repeat_char(self, item: Dict[str, Any], var_name: str = None) -> str:
		char = item['char']
		count = resolve_variable(item.get('count', 1), self.variables)
		value = char * count
		save_variable(var_name, value, self.variables)
		return value

	def repeat_type(self, item: Dict[str, Any], var_name: str = None) -> str:
		count = resolve_variable(item.get('count', 1), self.variables)
		results = [self.process_item(item['spec']) for _ in range(count)]
		value = ''.join(results)
		save_variable(var_name, results, self.variables)
		return value

	def process_loop(self, item: Dict[str, Any], var_name: str = None) -> str:
		count = resolve_variable(item.get('count', 1), self.variables)
		loop_results = []
		for i in range(count):
			save_variable(item.get('save_as'), i, self.variables)
			loop_results.append(self.generate_input(item['spec']))
		return ''.join(loop_results)

	def generate_space(self, item: Dict[str, Any], var_name: str = None) -> str:
		return self.repeat_char({'char': ' ', 'count': item.get('count', 1)}, var_name)

	def generate_newline(self, item: Dict[str, Any], var_name: str = None) -> str:
		return self.repeat_char({'char': '\n', 'count': item.get('count', 1)}, var_name)

	def process_item(self, item: Dict[str, Any]) -> str:
		item_type = item['type']
		var_name = item.get('save_as')

		handler = self.type_handlers.get(item_type)
		if handler:
			return handler(item, var_name)
		else:
			raise ValueError(f"Unknown item type: {item_type}")

	def generate_input(self, spec: List[Dict[str, Any]]) -> str:
		return ''.join(self.process_item(item) for item in spec)


def generate_input(spec: List[Dict[str, Any]]) -> str:
	generator = InputGenerator()
	input_data = generator.generate_input(spec)
	return input_data
