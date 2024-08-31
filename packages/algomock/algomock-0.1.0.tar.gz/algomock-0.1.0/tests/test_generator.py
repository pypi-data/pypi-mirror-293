from algomock import generate_input, generate_output_string


def main():
	spec = [
		{'type': 'int', 'limit': [1, 10]},  # 첫 번째 정수 (인덱스 0)
		{'type': 'int', 'limit': [1, 10]},  # 두 번째 정수 (인덱스 1)
		{'type': 'newline'},  # 줄 바꿈
		{'type': 'array', 'size': '$0', 'element_type': 'int', 'limit': [1, 100]},  # 배열 크기는 첫 번째 정수를 참조
		{'type': 'newline'},  # 줄 바꿈
		{'type': '2d_array', 'rows': '$1', 'cols': '$0', 'element_type': 'int', 'limit': [0, 100]},  # 2D 배열 크기는 이전 정수들을 참조
		{'type': 'newline'},  # 줄 바꿈
		{'type': 'string', 'length': '$0'}  # 문자열 길이는 첫 번째 정수를 참조
	]

	num_test_cases = 3

	all_test_cases = []
	all_test_cases.append(str(num_test_cases))

	for _ in range(num_test_cases):
		try:
			input_data = generate_input(spec)
			test_case_string = generate_output_string(input_data, spec)
			all_test_cases.append(test_case_string)
		except Exception as e:
			print(f"Error generating test case: {e}")

	final_output = '\n'.join(all_test_cases)
	print(final_output)


if __name__ == "__main__":
	main()

# 필요하다면 파일로 저장할 수 있습니다
# with open('test_cases.txt', 'w') as f:
#     f.write(final_output)
