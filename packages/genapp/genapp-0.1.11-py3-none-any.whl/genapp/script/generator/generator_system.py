import os

from genapp.script.util import file as Fl
from genapp.script.util import string as St

from . import constants as c

###########################################################
########################## Cache ##########################
###########################################################
THIS_PATH = os.path.dirname(os.path.abspath(__file__))

def generate(
    project_path,
    schema_file,
    database_name,
):
    try:
        generate_cache(project_path, schema_file, database_name)
        generate_authorization(project_path, schema_file, database_name)
        generate_token(project_path, schema_file, database_name)
        generate_audit(project_path, schema_file, database_name)
        generate_conn(project_path, schema_file, database_name)
        generate_login(project_path, schema_file, database_name)
        generate_payload(project_path, schema_file, database_name)

    except Exception as e:
        print("ERROR: Generator cache -> generate: " + str(e))


def generate_cache(project_path, schema_file, database_name, with_listener=False):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        if with_listener:
            content = Fl.read_file(path_schema, c.SCHEMA_CACHE_LISTENER_FILE)
        else:
            content = Fl.read_file(path_schema, c.SCHEMA_CACHE_FILE)

        path_out = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")

        funtionality_name = St.text_to_snake(os.getenv("API_FUNTIONALITY"))
        role_name = St.text_to_snake(os.getenv("API_ROLE"))

        funtionality_class = St.text_to_pascal(os.getenv("API_FUNTIONALITY"))
        role_class = St.text_to_pascal(os.getenv("API_ROLE"))

        file_name_conn = St.text_to_snake(os.getenv("API_CONNECTION"))
        class_name_conn = St.text_to_pascal(os.getenv("API_CONNECTION"))

        replace_list = [
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_FUNTIONALITY_KEY, funtionality_name),
            (c.API_FUNTIONALITY_CLASS_KEY, funtionality_class),
            (c.API_ROLE_KEY, role_name),
            (c.API_ROLE_CLASS_KEY, role_class),
            (c.API_CONNECTION_KEY, file_name_conn),
            (c.API_CONNECTION_CLASS_KEY, class_name_conn),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_CACHE,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_cache: " + str(e))


def generate_authorization(project_path, schema_file, database_name):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        content = Fl.read_file(path_schema, c.SCHEMA_AUTHORIZATION_FILE)

        path_service = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")
        path_middleware = os.path.join(path_service, f"{c.MIDDLEWARE}")
        path_out = os.path.join(path_middleware, f"{c.AUTH}")

        file_name_user = St.text_to_snake(os.getenv("API_USER"))
        class_name = St.text_to_pascal(os.getenv("API_USER"))

        replace_list = [
            (c.MODEL_KEY, c.MODEL),
            (c.SERVICE_KEY, c.SERVICE),
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.CLASS_NAME_KEY, class_name),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_USER_KEY, file_name_user),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_AUTH,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_authorization: " + str(e))


def generate_token(project_path, schema_file, database_name):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        content = Fl.read_file(path_schema, c.SCHEMA_TOKEN)

        path_service = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")
        path_request = os.path.join(path_service, f"{c.REQUEST}")
        path_out = os.path.join(path_request, f"{c.SYS}")

        file_name_user = St.text_to_snake(os.getenv("API_USER"))
        class_name = St.text_to_pascal(os.getenv("API_USER"))

        replace_list = [
            (c.MODEL_KEY, c.MODEL),
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.CLASS_NAME_KEY, class_name),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_USER_KEY, file_name_user),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_TOKEN,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_token: " + str(e))


def generate_audit(project_path, schema_file, database_name):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        content = Fl.read_file(path_schema, c.SCHEMA_AUDIT)

        path_service = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")
        path_middleware = os.path.join(path_service, f"{c.MIDDLEWARE}")
        path_out = os.path.join(path_middleware, f"{c.AUDIT}")

        file_name_request = St.text_to_snake(os.getenv("API_AUDIT_REQUEST"))
        class_name_request = St.text_to_pascal(os.getenv("API_AUDIT_REQUEST"))

        file_name_request_not_logged = St.text_to_snake(
            os.getenv("API_AUDIT_REQUEST_NOT_LOGGED")
        )
        class_name_request_not_logged = St.text_to_pascal(
            os.getenv("API_AUDIT_REQUEST_NOT_LOGGED")
        )

        file_name_response = St.text_to_snake(os.getenv("API_AUDIT_RESPONSE"))
        class_name_response = St.text_to_pascal(os.getenv("API_AUDIT_RESPONSE"))

        replace_list = [
            (c.MODEL_KEY, c.MODEL),
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_AUDIT_RESPONSE_KEY, file_name_response),
            (c.API_AUDIT_REQUEST_KEY, file_name_request),
            (c.API_AUDIT_REQUEST_NOT_LOGGED_KEY, file_name_request_not_logged),
            (c.API_AUDIT_RESPONSE_CLASS_KEY, class_name_response),
            (c.API_AUDIT_REQUEST_CLASS_KEY, class_name_request),
            (c.API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEY, class_name_request_not_logged),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_AUDIT,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_audit: " + str(e))


def generate_conn(project_path, schema_file, database_name):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        content = Fl.read_file(path_schema, c.SCHEMA_CONNECTION_FILE)

        path_service = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")
        path_middleware = os.path.join(path_service, f"{c.MIDDLEWARE}")
        path_out = os.path.join(path_middleware, f"{c.AUTH}")

        file_name_conn = St.text_to_snake(os.getenv("API_CONNECTION"))
        class_name_conn = St.text_to_pascal(os.getenv("API_CONNECTION"))

        file_name_request_not_logged = St.text_to_snake(
            os.getenv("API_AUDIT_REQUEST_NOT_LOGGED")
        )
        class_name_request_not_logged = St.text_to_pascal(
            os.getenv("API_AUDIT_REQUEST_NOT_LOGGED")
        )

        file_name_login = St.text_to_snake(os.getenv("API_LOGIN"))
        class_name_login = St.text_to_pascal(os.getenv("API_LOGIN"))

        replace_list = [
            (c.MODEL_KEY, c.MODEL),
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_CONNECTION_KEY, file_name_conn),
            (c.API_CONNECTION_CLASS_KEY, class_name_conn),
            (c.API_AUDIT_REQUEST_NOT_LOGGED_KEY, file_name_request_not_logged),
            (c.API_LOGIN_KEY, file_name_login),
            (c.API_LOGIN_CLASS_KEY, class_name_login),
            (c.API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEY, class_name_request_not_logged),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_CONN,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_conn: " + str(e))


def generate_login(project_path, schema_file, database_name):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        content = Fl.read_file(path_schema, c.SCHEMA_LOGIN_FILE)

        path_service = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")
        path_middleware = os.path.join(path_service, f"{c.MIDDLEWARE}")
        path_out = os.path.join(path_middleware, f"{c.AUDIT}")

        file_name_login = St.text_to_snake(os.getenv("API_LOGIN"))
        class_name_login = St.text_to_pascal(os.getenv("API_LOGIN"))

        replace_list = [
            (c.MODEL_KEY, c.MODEL),
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_LOGIN_KEY, file_name_login),
            (c.API_LOGIN_CLASS_KEY, class_name_login),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_LOGIN,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_login: " + str(e))


def generate_payload(project_path, schema_file, database_name):
    try:
        path_schema = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)

        content = Fl.read_file(path_schema, c.SCHEMA_PAYLOAD)

        path_service = os.path.join(project_path, f"{c.APP}\\{c.SERVICE}")
        path_middleware = os.path.join(path_service, f"{c.MIDDLEWARE}")
        path_out = os.path.join(path_middleware, f"{c.AUDIT}")

        file_name_login = St.text_to_snake(os.getenv("API_AUDIT_PAYLOAD"))
        class_name_login = St.text_to_pascal(os.getenv("API_AUDIT_PAYLOAD"))

        replace_list = [
            (c.MODEL_KEY, c.MODEL),
            (c.CRUD_KEY, c.CRUD),
            (c.SCHEMA_KEY, c.SCHEMA),
            (c.SCHEMA_DATABASE_KEY, schema_file),
            (c.DATABASE_NAME_KEY, database_name),
            (c.API_AUDIT_PAYLOAD_KEY, file_name_login),
            (c.API_AUDIT_PAYLOAD_CLASS_KEY, class_name_login),
        ]

        Fl.generate_file_from_schema(
            content_schema=content,
            file_name_out=c.FILE_NAME_PAYLOAD,
            path_out=path_out,
            replace_list=replace_list,
        )

    except Exception as e:
        print("ERROR: Generator cache -> generate_payload: " + str(e))
