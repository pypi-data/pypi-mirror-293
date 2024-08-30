import os
import subprocess
from genapp.script.util import path as Path


def get_absolute_path(directory):
    try:
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".py"):
                    yield os.path.join(root, file_name)
    except Exception as e:
        print("ERROR: Script clean code -> get_absolute_path: ", e)


def clean():
    try:
        # Ruta al directorio principal de tu proyecto
        project_directory = Path.get_previous_path(previous=2)
        print(project_directory)

        # Directorio donde se encuentran los archivos de Python dentro de tu proyecto
        app_directory = os.path.join(project_directory, "app")

        # Obtener la ruta absoluta de cada archivo .py en el directorio /app
        for file_path in get_absolute_path(app_directory):
            # Llamar a la herramienta absolufy-imports con la ruta absoluta del archivo como argumento
            subprocess.run(["absolufy-imports", file_path])

        # Formatear el archivo usando autopep8
        subprocess.run(["autopep8", "--in-place", "--recursive", project_directory])

    except Exception as e:
        print("ERROR: Script clean code -> clean: ", e)
