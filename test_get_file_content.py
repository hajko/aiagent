from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"Result for lorem.txt is {len(result)} characters.")
print(result[-(len(result) - 10000) :])

result = get_file_content("calculator", "main.py")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print(result)

result = get_file_content("calculator", "/bin/cat")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(result)
