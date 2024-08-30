import asyncio
from app.util import string as St
from app.service.controller import Controller
from app.service.response.header import HeaderAPI, HeaderKeys
from fastapi.encoders import jsonable_encoder

from app.service.middleware.decorator import notify
from app.service.response.result import ResultCodes


class RequestKeys:
    # Keys del contenido de una request
    HEADER = "header"
    BODY = "body"

    # Tipos de request
    POST = "post"
    GET = "get"


# Definimos la metaclase
class RequestMeta(type):
    def __new__(cls, name, bases, attrs):
        # Iteramos sobre todos los atributos de la clase
        for attr_name, attr_value in attrs.items():
            # Verificamos si el atributo es un método y si su nombre empieza con "_x"
            if callable(attr_value) and attr_name.startswith("x"):
                # Se aplica el decorador notify
                attrs[attr_name] = notify(attr_value)
        return super().__new__(cls, name, bases, attrs)


class Request(Controller, metaclass=RequestMeta):

    # Constantes KEYS que se pueden dar en peticiones GET por URL o en JSON por POST
    MODE = "mode"

    MODE_USER = "user"
    MODE_EMPLOYEE = "employee"
    MODE_ADMIN = "admin"

    LIMIT_QUERY = "limit"  # Key para determinar cuantas filas por consulta
    PAGE_QUERY = "page"  # Key para determinar el numero de paquete de filas

    # Limite de filas maximo para una query fraccionada
    MAX_QUERY_LIMIT = 20

    def __init__(self, id_funtionality, request):
        self.id_funtionality = id_funtionality
        self.request = request

    def get_mandatory_value_from_dict(self, content, key, miss_key_on=None):
        try:
            if isinstance(content[key], list):
                return content[key][0]
            else:
                return content[key]
        except (KeyError, IndexError) as e:
            error_msg = "Mandatory parameter not found"
            if miss_key_on:
                error_msg += " on " + miss_key_on + ": "
            else:
                error_msg += ": "
            self.response_error(description=error_msg + str(key))

    def get_posible_value_from_dict(self, content, key):
        try:
            if isinstance(content[key], list):
                return content[key][0]
            else:
                return content[key]
        except (KeyError, IndexError) as e:
            return None

    def get_offset_limit(self, content):
        try:
            page = content.get(self.PAGE_QUERY, None)
            page = (
                self.get_mandatory_value_from_dict(content, self.PAGE_QUERY)
                if page is not None
                else None
            )

            # Si hay page
            if page is not None:
                # Si hay limit coge el valor si no se le asigna el por defecto
                limit = content.get(self.LIMIT_QUERY, self.MAX_QUERY_LIMIT)
                if isinstance(limit, int):
                    return int(limit) * int(page), int(limit)
                else:
                    limit = self.get_mandatory_value_from_dict(
                        content, self.LIMIT_QUERY
                    )
                    return int(limit) * int(page), int(limit)

            # Si solo esta limit y no hay page
            limit = content.get(self.LIMIT_QUERY, None)
            if limit is not None:
                if isinstance(limit, int):
                    # Se devuelve la primera pagina con el limite establecido
                    return 0, int(limit)
                else:
                    limit = (
                        self.get_mandatory_value_from_dict(content, self.LIMIT_QUERY)
                        if limit is not None
                        else None
                    )
                    # Se devuelve la primera pagina con el limite establecido
                    return 0, int(limit)

        except Exception as e:
            print("ERROR: Request -> get_offset_limit: " + str(e))

        return None, None

    def check_version(self, header, min_version):
        try:
            if isinstance(header, dict):
                version = header.get(HeaderKeys.VERSION, None)

                return int(version) >= int(min_version)

        except Exception as e:
            print("ERROR: Request -> check_version: " + str(e))
        return False

    def get_lang_header(self, header, force_error=False):
        if force_error:
            lang = self.get_mandatory_value_from_dict(
                header, HeaderKeys.LANGUAGE, miss_key_on=RequestKeys.HEADER
            )
        else:
            lang = header.get(HeaderKeys.LANGUAGE, None)

        return St.text_to_snake(lang) if lang else None

    def get_version_header(self, header, force_error=False):
        if force_error:
            version = self.get_mandatory_value_from_dict(
                header, HeaderKeys.VERSION, miss_key_on=RequestKeys.HEADER
            )
        else:
            version = header.get(HeaderKeys.VERSION, None)

        return St.text_to_snake(version) if version else None

    def get_channel_header(self, header, force_error=False):
        if force_error:
            channel = self.get_mandatory_value_from_dict(
                header, HeaderKeys.CHANNEL, miss_key_on=RequestKeys.HEADER
            )
        else:
            channel = header.get(HeaderKeys.CHANNEL, None)

        return St.text_to_snake(channel) if channel else None

    def get_result_code_hasnext(self, has_next):
        if has_next:
            return ResultCodes.DATA_AVAILABLE
        else:
            return ResultCodes.NO_MORE_DATA

    # Dado una lista de diccionarios y una lista de claves para esos diccionarios,
    # los diccionarios de salida solo contentran las claves que estan en list_
    def clean_data(self, data, list_) -> dict:
        try:
            if data is not None:
                if isinstance(data, list) and isinstance(list_, list):
                    return [
                        {key: json_data[key] for key in list_ if key in json_data}
                        for json_data in data
                    ]

                if isinstance(data, dict) and isinstance(list_, list):
                    return {key: data[key] for key in list_ if key in data}

        except Exception as e:
            print("ERROR: Request -> clean_data: " + str(e))
        return None
