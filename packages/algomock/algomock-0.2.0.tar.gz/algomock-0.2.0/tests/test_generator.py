from algomock import InputGenerator

# Example usage
spec = [
	{'type': 'int', 'limit': [1, 5], 'save_as': '$T'},  # Number of test cases
	{'type': 'newline'},
	{'type': 'loop', 'count': '$T', 'save_as': '$test_case', 'spec': [
		{'type': 'int', 'limit': [1, 10], 'save_as': '$N'},  # N
		{'type': 'space'},
		{'type': 'int', 'limit': [1, '$N'], 'save_as': '$M'},  # M, upper limit depends on N
		{'type': 'newline'},
		{'type': 'repeat_char', 'char': '*', 'count': '$N', 'save_as': '$stars'},  # Repeat '*' N times
		{'type': 'newline'},
		{'type': 'repeat_type', 'count': '$M', 'spec': {  # Repeat a random digit M times
			'type': 'int',
			'limit': [0, 9]
		}, 'save_as': '$digits'},
		{'type': 'newline'},
		{'type': 'array', 'size': '$N', 'limit': [1, 100], 'save_as': '$array'},  # Array of size N
		{'type': 'newline'},
		{'type': '2d_array', 'rows': '$M', 'cols': '$N', 'limit': [0, 100], 'save_as': '$matrix'},  # 2D array of size M x N
		{'type': 'newline'},
		{'type': 'string', 'length': '$M', 'save_as': '$str'},  # String of length M
		{'type': 'newline'},
		{'type': 'int', 'limit': ['$test_case', '$test_case'], 'save_as': '$index'},  # An integer between 0 and the current loop index
		{'type': 'newline'}
	]}
]

try:
	generator = InputGenerator()
	input_data = generator.generate_input(spec)
	print(input_data)
	print("\nGenerated Variables:")
	for key, value in generator.variables.items():
		print(f"{key}: {value}")
except Exception as e:
	print(f"Error generating test case: {e}")
