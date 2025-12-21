from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_call_dict = {
        "get_files_info": lambda: get_files_info("./calculator", **function_call.args),
        "get_file_content": lambda: get_file_content(
            "./calculator", **function_call.args
        ),
        "write_file": lambda: write_file("./calculator", **function_call.args),
        "run_python_file": lambda: run_python_file(
            "./calculator", **function_call.args
        ),
    }

    if function_call.name not in function_call_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    else:
        function_result = function_call_dict[function_call.name]()

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": function_result},
            )
        ],
    )
