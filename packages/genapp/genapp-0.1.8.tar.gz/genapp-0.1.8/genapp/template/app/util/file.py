import os
import re


def new_file(path, file_name, content):
    try:
        new_directory(path)
        with open(os.path.join(path, f"{file_name}.py"), "w", encoding="utf-8") as file:
            file.write(content)

    except Exception as e:
        print("ERROR Util file -> new_file: " + str(e))


def write_lines(path, file_name, lines, format=None):
    try:
        if not format:
            format = "py"

        path_file = os.path.join(path, f"{file_name}.{format}")
        with open(path_file, "w", encoding="utf-8") as file:
            file.writelines(lines)

    except Exception as e:
        print("ERROR Util file -> write_lines: " + str(e))


def read_file(path, file_name, format=None):
    try:
        if not format:
            format = "py"

        if exist_file(path, file_name, format):
            with open(
                os.path.join(path, f"{file_name}.{format}"), "r", encoding="utf-8"
            ) as file:
                content = file.read()

            return content

    except Exception as e:
        print("ERROR Util file -> read_file: " + str(e))

    return None


def read_lines(path, file_name, format=None):
    try:
        if not format:
            format = "py"

        if exist_file(path, file_name, format):
            path_file = os.path.join(path, f"{file_name}.{format}")
            with open(path_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            return lines

    except Exception as e:
        print("ERROR Util file -> read_lines: " + str(e))

    return None


def new_directory(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)

    except Exception as e:
        print("ERROR Util file -> new_directory: " + str(e))


def exist_file(path, file_name, format=None):
    try:
        if not format:
            format = "py"

        file = os.path.join(path, file_name + "." + format)
        return os.path.exists(file)

    except Exception as e:
        print("ERROR Util file -> exist_file: " + str(e))


def exist_directory(path):
    try:
        return os.path.isdir(path)
    except Exception as e:
        print("ERROR Util file -> exist_directory: " + str(e))

def generate_file_from_schema(
    content_schema=None, file_name_out=None, path_out=None, replace_list: list = None
):
    try:
        for element in replace_list:
            key, new_content = element
            content_schema = re.sub(
                re.escape(key), new_content, content_schema)

        new_file(path_out, file_name_out, content_schema)

    except Exception as e:
        print("ERROR Util file -> generate_file_from_schema: " + str(e))
