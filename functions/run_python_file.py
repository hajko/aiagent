import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
        command.extend(args)

    result = subprocess.run(
        command,
        cwd="/Users/julianong/aiagent",
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = []
    if result.returncode != 0:
        output.append(f"Process exited with code {result.returncode}\n")
        if result.stdout == "" and result.stderr == "":
            output.append("No output produced\n")
    else:
        output.append(f"STDOUT: {result.stdout}")
        output.append(f"STDERR: {result.stderr}")

    return "".join(output)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments in string format",
                items=types.Schema(
                    type=types.Type.STRING, description="An argument in string format"
                ),
            ),
        },
    ),
)
