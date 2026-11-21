import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_target_directory = os.path.normpath(os.path.join(absolute_working_directory, directory))
      
        # adding error conditions
        if os.path.commonpath([absolute_working_directory, absolute_target_directory]) != absolute_working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(absolute_target_directory):
            return f'Error: "{directory}" is not a directory'

        absolute_sub_directory = map(lambda target: os.path.normpath(os.path.join(absolute_target_directory, target)), os.listdir(absolute_target_directory))
        # creates string with information about sub-files
        files_info = ("\n".join(map(
                lambda target: f"- {os.path.basename(target)}: file_size={os.path.getsize(target)} bytes, is_dir={os.path.isdir(target)}",
                    absolute_sub_directory
            )))

        return f"Result for {"current" if directory == "." else directory} directory:\n{files_info}"

    except Exception as e:
        return f"Error: {e}"
