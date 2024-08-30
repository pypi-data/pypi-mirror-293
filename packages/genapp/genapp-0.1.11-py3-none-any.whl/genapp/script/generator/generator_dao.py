import os

from genapp.script.util import file as Fl
from genapp.script.util import string as St

from . import constants as c

###########################################################
########################### DAO ###########################
###########################################################
THIS_PATH = os.path.dirname(os.path.abspath(__file__))


def generate(
    overwrite, file_name, class_name, database, database_class, schema_file, path
):
    try:
        DAO_EXTENSION = "_dao"
        dao_file_name = file_name + DAO_EXTENSION

        user_file_name = St.text_to_snake(os.getenv("API_USER"))
        role_file_name = St.text_to_snake(os.getenv("API_ROLE"))
        funtionality_file_name = St.text_to_snake(os.getenv("API_FUNTIONALITY"))
        conn_file_name = St.text_to_snake(os.getenv("API_CONNECTION"))
        login_file_name = St.text_to_snake(os.getenv("API_LOGIN"))

        if file_name in [
            user_file_name,
            role_file_name,
            funtionality_file_name,
            conn_file_name,
            login_file_name,
        ]:
            if file_name == funtionality_file_name:
                schema = c.SCHEMA_FUNTIONALITY_DAO_FILE

            elif file_name == role_file_name:
                schema = c.SCHEMA_ROLE_DAO_FILE

            elif file_name == user_file_name:
                schema = c.SCHEMA_USER_DAO_FILE

            elif file_name == conn_file_name:
                schema = c.SCHEMA_CONNECTION_DAO_FILE

            elif file_name == login_file_name:
                schema = c.SCHEMA_LOGIN_DAO_FILE

            path_script_schemas = os.path.join(THIS_PATH, c.ROUTE_SCHEMAS_GENERATOR)
            
            content = Fl.read_file(path_script_schemas, schema)
            
            replace_list = [
                (c.DATABASE_NAME_KEY, database),
                (c.DATABASE_CLASS_KEY, database_class),
                (c.SCHEMA_DATABASE_KEY, schema_file),
                (c.MODEL_KEY, c.MODEL),
                (c.CRUD_KEY, c.CRUD),
                (c.DATABASE_KEY, c.DATABASE),
                (c.SCHEMA_KEY, c.SCHEMA),
                (c.CLASS_NAME_KEY, class_name),
                (c.FILE_NAME_KEY, file_name),
                (c.API_ROLE_CLASS_KEY, St.text_to_pascal(os.getenv("API_ROLE"))),
                (c.API_SCOPE_CLASS_KEY, St.text_to_pascal(os.getenv("API_SCOPE"))),
                (
                    c.API_CONNECTION_CLASS_KEY,
                    St.text_to_pascal(os.getenv("API_CONNECTION")),
                ),
                (c.API_LOGIN_CLASS_KEY, St.text_to_pascal(os.getenv("API_LOGIN"))),
                (
                    c.API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEY,
                    St.text_to_pascal(os.getenv("API_AUDIT_REQUEST_NOT_LOGGED")),
                ),
                (
                    c.API_FUNTIONALITY_PERMISSION_KEY,
                    St.text_to_snake(os.getenv("API_FUNTIONALITY_PERMISSION")),
                ),
                (
                    c.API_ROLE_PERMISSION_KEY,
                    St.text_to_snake(os.getenv("API_ROLE_PERMISSION")),
                ),
                (c.API_ROLE_SCOPE_KEY, St.text_to_snake(os.getenv("API_ROLE_SCOPE"))),
                (c.API_PERMISSION_KEY, St.text_to_snake(os.getenv("API_PERMISSION"))),
                (c.API_USER_SCOPE_KEY, St.text_to_snake(os.getenv("API_USER_SCOPE"))),
                (c.API_CONNECTION_KEY, St.text_to_snake(os.getenv("API_CONNECTION"))),
                (c.API_LOGIN_KEY, St.text_to_snake(os.getenv("API_LOGIN"))),
                (
                    c.API_AUDIT_REQUEST_NOT_LOGGED_KEY,
                    St.text_to_snake(os.getenv("API_AUDIT_REQUEST_NOT_LOGGED")),
                ),
            ]
            
            Fl.generate_file_from_schema(
                content_schema=content,
                file_name_out=dao_file_name,
                path_out=path,
                replace_list=replace_list,
            )
            
        else:
            # Construye el contenido del archivo
            content = IMPORTS
            content += import_database(database, database_class)
            content += import_schema(schema_file)
            content += importPydacticModel(database, file_name, class_name)
            content += init_class(class_name)
            content += builder(database_class)
            content += exampleDef(database_class, class_name)
            content += getCondition(database_class, class_name)
            content += initObjectSQL(database_class, class_name)

            for crud in c.CRUDS:
                content += f"    {crud_def(class_name, crud)}\n"

            if overwrite or not Fl.exist_file(path, dao_file_name):
                Fl.new_file(path, dao_file_name, content)

    except Exception as e:
        print("ERROR: Generator dao -> generate: " + str(e))


# Constantes para todos los DAO
IMPORTS = (
    f"from {c.APP}.crud.dao import Dao\n"
    + "from fastapi.encoders import jsonable_encoder\n"
    + "from sqlalchemy import and_, or_\n"
    + "from sqlalchemy.future import select\n"
)


def crud_def(class_name, crud_type):
    if crud_type == "query":
        return f"""async def query(self, elementPydantic, output_format=None):
        conditions = self._getCondition(elementPydantic)
        return await super().query({class_name}, conditions, output_format=output_format)\n"""
    else:
        return f"""async def {crud_type}(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().{crud_type}(element)\n"""


def exampleDef(database_class, class_name):
    return f"""    # async def getSomething(self, elementPydantic, date_init, date_end):
    #     try:
    #         select = []

    #         select.append({class_name}.attribute1)
    #         select.append({class_name}.attribute2)
    #         # select.append({class_name}.attribute3)
    #         select.append({class_name}.attribute4)

    #         conditions = self._getCondition(elementPydantic)
    #         conditions.append({class_name}.date.between(date_init, date_end))
    #         conditions.append({class_name}.attribute1 == 100)

    #         return await super().query({class_name}, conditions, select)

    #     except Exception as e:
    #         print(f"ERROR: {database_class} {class_name}Dao -> getSomething: " + str(e))
    #         return e\n\n"""


def init_class(class_name):
    return f"\nclass {class_name}Dao(Dao):\n"


def builder(database_class):
    return f"""    def __init__(self):
        self.database = {database_class}()
        self.conn = self.database.newConn()\n\n"""


def initObjectSQL(database_class, class_name):
    return f"""    def _initObjectSQLAlchemy(self, elementPydantic):
        try:
            attributes = elementPydantic.model_dump(exclude_none=True, exclude_unset=True)
            return {class_name}(**attributes)
        except Exception as e:
            print(f"ERROR: {database_class} {class_name}Dao -> initObjectSQLAlchemy: " + str(e))
        return None\n\n"""


def getCondition(database_class, class_name):
    return f"""    def _getCondition(self, elementPydantic):
        try:
            conditions = []
            for attribute_name, attribute_value in elementPydantic.__dict__.items():
                if attribute_value is not None:
                    sqlalchemy_condition = getattr({class_name}, attribute_name) == attribute_value
                    conditions.append(sqlalchemy_condition)
            if conditions:
                return conditions
            else:
                return None
            
        except Exception as e:
            print(f"ERROR: {database_class} {class_name}Dao -> getCondition: " + str(e))
        return None\n\n"""


def importPydacticModel(database, file_name, class_name):
    return f"from {c.APP}.{c.MODEL}.{database}.{file_name} import {class_name}Model\n"


def import_database(database, database_class):
    return f"from {c.APP}.{c.DATABASE}.{database} import {database_class}\n"


def import_schema(schema_file):
    return f"from {c.APP}.{c.CRUD}.{c.SCHEMA}.{schema_file} import *\n"
