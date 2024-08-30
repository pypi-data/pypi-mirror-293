import inspect
import os
from pathlib import Path


def get_current_path():
    try:
        frame = inspect.stack()[1]
        # Obtener el path del archivo que llama a esta función
        caller_file = frame.filename
        # Obtener la ruta absoluta del archivo
        caller_path = os.path.abspath(caller_file)
        # Obtener el directorio del archivo
        caller_dir = os.path.dirname(caller_path)
        return caller_dir
    except Exception as e:
        print("ERROR Util path -> get_current_path: " + str(e))


def get_previous_path(path=None, previous=1):
    try:
        if not path:
            path = get_current_path()
        if previous > 0:
            return get_previous_path(os.path.dirname(path), previous - 1)
        else:
            return path
    except Exception as e:
        print("ERROR Util path -> get_previous_path: " + str(e))

    return None


def get_path_file(path, file_name):
    try:
        return os.path.join(path, file_name)
    except Exception as e:
        print("ERROR Util path -> get_path_file: " + str(e))


def get_files_info(path, exclude_subdirectories=[]):
    try:
        files_info = []
        # Recorre el directorio y sus subdirectorios
        for root, dirs, files in os.walk(path):
            # Filtra los directorios que comienzan con '_'
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith("_") and d not in exclude_subdirectories
            ]
            for file in files:
                # Obtiene el nombre del archivo y su ruta completa
                file_name, file_extension = os.path.splitext(file)
                # Agrega el nombre del archivo (sin extensión) y el nombre del subdirectorio al diccionario
                file_info = {
                    "name": file_name,
                    "package": os.path.relpath(root, path),
                }
                files_info.append(file_info)
        return files_info

    except Exception as e:
        print("ERROR Util path -> get_files_info: " + str(e))


def get_path_absolute(path_relative) -> str:
    try:
        path = Path(path_relative)
        return path.resolve()

    except Exception as e:
        print("ERROR Util path -> get_path_absolute: " + str(e))
