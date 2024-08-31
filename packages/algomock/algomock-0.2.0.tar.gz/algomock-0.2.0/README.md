# AlgoMock

AlgoMock is a flexible and powerful input generator for algorithm testing and competitive programming. It allows you to easily create mock input data for various algorithm problems, helping you test your solutions more efficiently.

## Features

- Generate various types of input: integers, strings, arrays, and 2D arrays
- Define input specifications using a simple and intuitive format
- Reference previously generated values in your specifications
- Customizable output format
- Support for loops and repetition in input generation

## Installation

You can install AlgoMock using pip:

```
pip install algomock
```

## Quick Start

Here's a simple example of how to use AlgoMock:

```python
from algomock import generate_input

spec = [
    {'type': 'int', 'limit': [1, 10], 'save_as': '$N'},  # N
    {'type': 'space'},
    {'type': 'int', 'limit': [1, 10], 'save_as': '$M'},  # M
    {'type': 'newline'},
    {'type': 'array', 'size': '$N', 'element_type': 'int', 'limit': [1, 100]},  # Array of size N
    {'type': 'newline'},
    {'type': '2d_array', 'rows': '$M', 'cols': '$N', 'element_type': 'int', 'limit': [0, 100]},  # 2D array of size M x N
]

input_data = generate_input(spec)
print(input_data)
```

This will generate input data according to the specification and print it in a format suitable for most algorithm problems.

## Detailed Usage

AlgoMock uses a list of dictionaries to specify the input format. Each dictionary represents one element of the input. Below is a detailed explanation of each input type and how to use them.

### Integer (`int`)

Generates a random integer within a specified range.

**Parameters:**
- `type`: Set to `'int'`
- `limit`: A list of two integers `[min, max]` specifying the range (inclusive)
- `save_as` (optional): A variable name to save the generated value for later reference

**Example:**
```python
{'type': 'int', 'limit': [1, 100], 'save_as': '$N'}
```
This will generate a random integer between 1 and 100 (inclusive) and save it as `$N` for later reference.

### Array (`array`)

Generates an array of random integers.

**Parameters:**
- `type`: Set to `'array'`
- `size`: The size of the array (can be a fixed number or a reference to a previously saved variable)
- `element_type`: Currently only supports `'int'`
- `limit`: A list of two integers `[min, max]` specifying the range for each element (inclusive)
- `save_as` (optional): A variable name to save the generated array for later reference

**Example:**
```python
{'type': 'array', 'size': '$N', 'element_type': 'int', 'limit': [1, 1000], 'save_as': '$arr'}
```
This will generate an array of `$N` integers, each between 1 and 1000, and save it as `$arr`.

### 2D Array (`2d_array`)

Generates a 2D array (matrix) of random integers.

**Parameters:**
- `type`: Set to `'2d_array'`
- `rows`: The number of rows in the 2D array
- `cols`: The number of columns in the 2D array
- `element_type`: Currently only supports `'int'`
- `limit`: A list of two integers `[min, max]` specifying the range for each element (inclusive)
- `save_as` (optional): A variable name to save the generated 2D array for later reference

**Example:**
```python
{'type': '2d_array', 'rows': '$M', 'cols': '$N', 'element_type': 'int', 'limit': [0, 100], 'save_as': '$matrix'}
```
This will generate a 2D array with `$M` rows and `$N` columns, filled with integers between 0 and 100, and save it as `$matrix`.

### String (`string`)

Generates a random string of lowercase letters.

**Parameters:**
- `type`: Set to `'string'`
- `length`: The length of the string (can be a fixed number or a reference to a previously saved variable)
- `save_as` (optional): A variable name to save the generated string for later reference

**Example:**
```python
{'type': 'string', 'length': 10, 'save_as': '$str'}
```
This will generate a random string of 10 lowercase letters and save it as `$str`.

### Newline (`newline`)

Inserts a newline character.

**Parameters:**
- `type`: Set to `'newline'`

**Example:**
```python
{'type': 'newline'}
```
This will insert a newline character in the output.

### Space (`space`)

Inserts a single space character.

**Parameters:**
- `type`: Set to `'space'`

**Example:**
```python
{'type': 'space'}
```
This will insert a single space character in the output.

### Repeat Character (`repeat_char`)

Repeats a specified character a given number of times.

**Parameters:**
- `type`: Set to `'repeat_char'`
- `char`: The character to repeat
- `count`: The number of times to repeat the character
- `save_as` (optional): A variable name to save the generated string for later reference

**Example:**
```python
{'type': 'repeat_char', 'char': '*', 'count': '$N', 'save_as': '$stars'}
```
This will repeat the `*` character `$N` times and save the result as `$stars`.

### Repeat Type (`repeat_type`)

Repeats a specified input type generation a given number of times.

**Parameters:**
- `type`: Set to `'repeat_type'`
- `count`: The number of times to repeat the specified input type
- `spec`: The specification of the input type to repeat
- `save_as` (optional): A variable name to save the generated values for later reference

**Example:**
```python
{'type': 'repeat_type', 'count': '$M', 'spec': {'type': 'int', 'limit': [0, 9]}, 'save_as': '$digits'}
```
This will generate `$M` random digits (0-9) and save them as `$digits`.

### Loop (`loop`)

Repeats a set of input specifications a specified number of times.

**Parameters:**
- `type`: Set to `'loop'`
- `count`: The number of times to repeat the loop
- `spec`: A list of input specifications to repeat
- `save_as` (optional): A variable name to save the current loop index for use within the loop

**Example:**
```python
{'type': 'loop', 'count': '$T', 'save_as': '$test_case', 'spec': [
    {'type': 'int', 'limit': [1, 100], 'save_as': '$N'},
    {'type': 'space'},
    {'type': 'array', 'size': '$N', 'element_type': 'int', 'limit': [1, 1000]},
    {'type': 'newline'}
]}
```
This will repeat the generation of an integer `$N`, a space, and an array of size `$N` for `$T` times, representing `$T` test cases.

## Advanced Example

Here's a comprehensive example that demonstrates the use of various input types:

```python
from algomock import InputGenerator

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
        {'type': 'int', 'limit': [0, '$test_case'], 'save_as': '$index'},  # An integer between 0 and the current loop index
        {'type': 'newline'}
    ]}
]

generator = InputGenerator()
input_data = generator.generate_input(spec)
print(input_data)
```

This example generates multiple test cases, each with various types of input data, demonstrating the flexibility of AlgoMock.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.