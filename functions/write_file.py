import os
import re

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a specified file relative to the working directory, overwrites the original file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text which overwrites the original file",
                },
            },
        },
    },
}
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try: 
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_target_directory = os.path.normpath(os.path.join(absolute_working_directory, file_path))

        if os.path.commonpath([absolute_working_directory, absolute_target_directory]) != absolute_working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'            
        if os.path.isdir(absolute_target_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        os.makedirs(os.path.dirname(absolute_target_directory), exist_ok=True)
        with open(absolute_target_directory, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
