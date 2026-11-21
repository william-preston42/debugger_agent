import os
from os.path import join
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified python file (and only python files) relative to the working directory, returns the return code and the STDOUT and STDERR output (if there is any)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to python file to run, relative to the working directory",
                },
                "args": {
                "type": "array[str]",
                "description": "Extra arguments which can be passed to the file to run, default is None",
                },
            },
        },
    },
}
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_target_directory = os.path.normpath(os.path.join(absolute_working_directory, file_path))
      
        # adding error conditions
        if os.path.commonpath([absolute_working_directory, absolute_target_directory]) != absolute_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 
        if not os.path.isfile(absolute_target_directory):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_target_directory]
        if args is not None:
            command.extend(args)
        
        command_result = subprocess.run(
            command, 
            cwd=absolute_working_directory, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        output_string = []
        if command_result.returncode != 0:
            output_string.append(f"Process exited with code {command_result.returncode}")
        if not command_result.stdout and not command_result.stderr:
            output_string.append("No output produced")
        if command_result.stdout:
            output_string.append(f"STDOUT: {command_result.stdout}")
        if command_result.stderr:
            output_string.append(f"STDERR: {command_result.stderr}")

        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"
