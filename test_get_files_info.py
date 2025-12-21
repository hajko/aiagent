from functions.get_files_info import get_files_info

# print("Result for current directory:")
# for line in get_files_info("calculator", ".").split("\n"):
#    print(f"  {line}")
# print("Result for 'pkg' directory:")
# for line in get_files_info("calculator", "pkg").split("\n"):
#     print(f"  {line}")
# print("Result for 'bin' directory:")
# for line in get_files_info("calculator", "/bin").split("\n"):
#     print(f"    {line}")
# print("Result for '../' directory:")
# for line in get_files_info("calculator", "../").split("\n"):
#     print(f"    {line}")
result = get_files_info("calculator", ".")
print("Result for current directory:")
print(result)

result = get_files_info("calculator", "pkg")
print("Result for 'pkg directory:")
print(result)

result = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(result)

result = get_files_info("calculator", "../")
print("Result for '../' directory:")
print(result)
