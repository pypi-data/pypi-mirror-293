# AlgoMock

AlgoMock is a flexible and powerful input generator for algorithm testing and competitive programming. It allows you to easily create mock input data for various algorithm problems, helping you test your solutions more efficiently.

## Features

- Generate various types of input: integers, floats, strings, arrays, and 2D arrays
- Define input specifications using a simple and intuitive format
- Reference previously generated values in your specifications
- Customizable output format

## Installation

You can install AlgoMock using pip:

```
pip install algomock
```

## Quick Start

Here's a simple example of how to use AlgoMock:

```python
from algomock import generate_input, generate_output_string

spec = [
    {'type': 'int', 'limit': [1, 10]},  # N
    {'type': 'int', 'limit': [1, 10]},  # M
    {'type': 'newline'},
    {'type': 'array', 'size': '$0', 'element_type': 'int', 'limit': [1, 100]},  # Array of size N
    {'type': 'newline'},
    {'type': '2d_array', 'rows': '$1', 'cols': '$0', 'element_type': 'int', 'limit': [0, 100]},  # 2D array of size M x N
]

input_data = generate_input(spec)
output_string = generate_output_string(input_data, spec)
print(output_string)
```

This will generate input data according to the specification and print it in a format suitable for most algorithm problems.

## Detailed Usage

### Input Specification

AlgoMock uses a list of dictionaries to specify the input format. Each dictionary represents one element of the input and can have the following keys:

- `type`: The type of the input element. Can be 'int', 'float', 'string', 'array', '2d_array', or 'newline'.
- `limit`: A list of two elements [min, max] specifying the range for numeric types or array elements.
- `size`: For arrays, specifies the size of the array.
- `rows` and `cols`: For 2D arrays, specify the number of rows and columns.
- `element_type`: For arrays and 2D arrays, specifies the type of the elements.
- `length`: For strings, specifies the length of the string.
- `char_set`: For strings, optionally specifies the set of characters to use (default is lowercase letters).

### Referencing Previous Values

You can reference previously generated values in your specification using the `$index` syntax, where `index` is the 0-based index of the previously generated value.

### Advanced Example

Here's a more advanced example that demonstrates various features of AlgoMock:

```python
from algomock import generate_input, generate_output_string

spec = [
    {'type': 'int', 'limit': [1, 10]},  # N
    {'type': 'int', 'limit': [1, 5]},   # M
    {'type': 'newline'},
    {'type': 'array', 'size': '$0', 'element_type': 'int', 'limit': [1, 1000]},  # Array of size N
    {'type': 'newline'},
    {'type': '2d_array', 'rows': '$1', 'cols': '$0', 'element_type': 'int', 'limit': [0, 100]},  # 2D array of size M x N
    {'type': 'newline'},
    {'type': 'string', 'length': '$1', 'char_set': 'ABCDEF'},  # String of length M
]

num_test_cases = 3

print(num_test_cases)
for _ in range(num_test_cases):
    input_data = generate_input(spec)
    output_string = generate_output_string(input_data, spec)
    print(output_string)
```

This will generate 3 test cases, each containing two integers N and M, an array of N integers, a 2D array of size M x N, and a string of length M.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.