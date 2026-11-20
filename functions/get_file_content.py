import os

from config import MAX_CHARACTERS

def get_file_content(working_directory: str, file_path: str) -> str:
    try: 
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_target_directory = os.path.normpath(os.path.join(absolute_working_directory, file_path))


        if os.path.commonpath([absolute_working_directory, absolute_target_directory]) != absolute_working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_target_directory):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(absolute_target_directory, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS) 
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        return file_content_string

    except Exception as e:
         return f"Error: {e}"
