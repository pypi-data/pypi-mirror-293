from app.util import string as St
from app.util import path as Path
import importlib
from importlib.util import find_spec

APP_PATH = "app"
CRUD_PATH = "crud"
MODEL_PATH = "model"
SERVICE_PATH = "service"
REQUEST_PATH = "request"
FUNTIONALITY_PATH = "funtionality"
WEB_PATH = "web"
EXTERNAL_API_PATH = "external_api"


DAO_CLASS = "Dao"
DAO_EXTENSION = "_dao"


def instance_object(
    directory_list, name, package=None, class_name=None, params=None, body=None
):
    """Instancia un objeto dado un directorio, paquete, nombre

    Args:
        directory_name (str): subdirectorio dentro de /app. Ejm: crud, model ...
        package (str): nombre del paquete dentro del subdirectorio
        name (str): nombre del modulo
    """
    try:
        module_name = St.text_to_snake(name)

        if not class_name:
            module_class = St.text_to_pascal(name)
        else:
            module_class = class_name

        if not package:
            directory_list = [APP_PATH] + directory_list + [module_name]
        else:
            directory_list = [APP_PATH] + directory_list + [package, module_name]

        module_path = St.get_module(directory_list)

        # Intentar encontrar el módulo especificado
        spec = find_spec(module_path)
        if spec is None:
            raise ImportError(f"No se pudo encontrar el módulo: {module_path}")

        # Importar el módulo dinámicamente
        module = importlib.import_module(module_path)

        # Obtener la clase especificada del módulo
        class_object = getattr(module, module_class)

        if params is not None:
            return class_object(*params)

        if body is not None:
            return class_object(**body)

        return class_object()

    except Exception as e:
        print("ERROR: Util object -> instance_object: " + str(e))
        print(module_path)
        return e


def instance_dao(package, name):
    """Instancia un objeto dao

    Args:
        package (str): nombre del paquete dentro de crud/
        name (str): nombre del modulo
    """
    try:
        name = name + DAO_EXTENSION
        return instance_object(directory_list=[CRUD_PATH], name=name, package=package)
    except Exception as e:
        print("ERROR: Util object -> instance_dao: " + str(e))
        return e


INSERT_MODEL_CLASS = "InsertModel"
UPDATE_MODEL_CLASS = "UpdateModel"
DELETE_MODEL_CLASS = "DeleteModel"
GENERIC_MODEL_CLASS = "Model"


def get_model_crud_type(crud_type):
    if crud_type == "insert":
        return INSERT_MODEL_CLASS
    if crud_type == "update":
        return UPDATE_MODEL_CLASS
    if crud_type == "delete":
        return DELETE_MODEL_CLASS
    if crud_type == "query":
        return GENERIC_MODEL_CLASS


def instance_model(package, name, crud_type, body={}):
    """Instancia un objeto pydantic en model

    Args:
        package (str): nombre del paquete dentro de model/
        name (str): nombre del modulo
        crud_type (str): tipo de crud a importar: query, insert, update, delete
    """
    # try:
    pydantic_class = get_model_crud_type(crud_type)
    class_name = St.text_to_pascal(name + pydantic_class)
    return instance_object(
        directory_list=[MODEL_PATH],
        name=name,
        package=package,
        class_name=class_name,
        body=body,
    )
    # except Exception as e:
    #     print("ERROR: Util object -> instance_model: " + str(e))
    #     return e


def instance_request(name, params, path=None):
    """Instancia un objeto request

    Args:
        package (str): nombre del paquete dentro de service/request/funtionality/
        name (str): nombre del modulo
    """
    try:
        if not path:
            path = FUNTIONALITY_PATH

        return instance_object(
            directory_list=[SERVICE_PATH, REQUEST_PATH, path],
            name=name,
            params=params,
        )
    except Exception as e:
        print("ERROR: Util object -> instance_request: " + str(e))
        return e


def instance_request_web(name, params):
    """Instancia un objeto request

    Args:
        package (str): nombre del paquete dentro de service/request/web/
        name (str): nombre del modulo
    """
    try:
        return instance_object(
            directory_list=[SERVICE_PATH, REQUEST_PATH, WEB_PATH],
            name=name,
            params=params,
        )
    except Exception as e:
        print("ERROR: Util object -> instance_request_web: " + str(e))
        return e


def instance_external_api(name, params):
    """Instancia un objeto external_api

    Args:
        package (str): nombre del paquete dentro de external_api/
        name (str): nombre del modulo
    """
    try:
        return instance_object(
            directory_list=[EXTERNAL_API_PATH], name=name, params=params
        )
    except Exception as e:
        print("ERROR: Util object -> instance_external_api: " + str(e))
        return e
