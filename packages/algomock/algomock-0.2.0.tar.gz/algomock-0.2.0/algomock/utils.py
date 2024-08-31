import random
import string
from typing import Union, Any, Dict, List


def resolve_variable(value: Union[int, str], variables: Dict[str, Any]) -> Any:
	if isinstance(value, str) and value.startswith('$'):
		return variables.get(value, value)
	return value


def save_variable(var_name: str, value: Any, variables: Dict[str, Any]):
	if var_name and var_name.startswith('$'):
		variables[var_name] = value


def generate_random_int(min_val: int, max_val: int) -> int:
	return random.randint(min_val, max_val)


def generate_random_string(length: int) -> str:
	return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_random_array(size: int, min_val: int, max_val: int) -> List[int]:
	return [random.randint(min_val, max_val) for _ in range(size)]


def generate_random_2d_array(rows: int, cols: int, min_val: int, max_val: int) -> List[List[int]]:
	return [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]
