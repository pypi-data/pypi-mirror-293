import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.dialects.mssql import *

from .util import file as Fl
from .util import string as St

from genapp.script.generator import constants as c
from genapp.script.generator import generator_system as gen_system
from genapp.script.generator import generator_dao as gen_dao
from genapp.script.generator import generator_funtionalities as gen_fun
from genapp.script.generator import generator_pydantic as gen_model
from genapp.script.generator.database.connection.connection import Connection
from genapp.script.generator.lib.sqlacodegen_v2 import external as codegen


"""
└───app
    ├───crud <- CRUD
    │   ├───schema <- SCHEMA
    ├───database <- DATABASE (Obligatorio)
    │   └───connection <- (Obligatorio)
    ├───lib
    │   └───sqlacodegen_v2
    ├───model <- MODEL
    ├───script
    ├───service
    └───util
"""

SCHEMA_DATABASE_FILE = "schema_"


def generate_system(project_path, database_name):
    schema_file = f"{SCHEMA_DATABASE_FILE}{database_name}"

    gen_system.generate(
        project_path,
        schema_file,
        database_name,
    )


def generate_model(
    database_api,
    project_path,
    database_to_read=None,
    overwrite_dao=False,
    overwrite_model=False,
    overwrite_schema=False,
    update_funtionalities=False,
):
    try:
        if isinstance(database_api, Connection):
            database_class = St.text_to_pascal(database_api.alias)
            conn = database_api.newConn(generator=True)
            # Nombre del fichero que define la conexion a una BBDD
            database_name = St.text_to_snake(database_api.alias)
            print("API database: " + str(database_name))
            # Cuando se quiera incluir una base de datos externa (Una que no sea la de gestion de la api, una MERE o un Tarsys por ejm, la de la api: Avre)
            if database_to_read:
                if isinstance(database_to_read, Connection):
                    conn = database_to_read.newConn(generator=True)
                    # Nombre del fichero que define la conexion a una BBDD
                    database_name = St.text_to_snake(database_to_read.alias)
                    database_class = St.text_to_pascal(database_to_read.alias)
                    print("Second database: " + str(database_name))
                    pass

            path_dao = os.path.join(project_path, f"{c.APP}\\{c.CRUD}\\{database_name}")

            Fl.new_directory(path_dao)

            path_model = os.path.join(
                project_path, f"{c.APP}\\{c.MODEL}\\{database_name}"
            )
            Fl.new_directory(path_model)

            path_schema = os.path.join(project_path, f"{c.APP}\\{c.CRUD}\\{c.SCHEMA}")
            Fl.new_directory(path_schema)

            schema_file = f"{SCHEMA_DATABASE_FILE}{database_name}"

            engine = create_engine(conn)

            if overwrite_schema:
                codegen.generate_models(
                    engine=engine, path=path_schema, file_name=schema_file
                )  # Genera el schema SQLAlchemy
                pass

            metadata = MetaData()
            metadata.reflect(bind=engine)

            tables = []

            for table in metadata.sorted_tables:
                if not (len(table.columns) == len(table.foreign_keys)) and not (
                    len(table.primary_key) == 0
                ):
                    file_name = St.text_to_snake(table.name)
                    # Se le pasa el nombre en snake_case para que luego sea reversible y viceversa
                    class_name = St.text_to_pascal(file_name)
                    # print(
                    #     str(table.name)
                    #     + " -> nombre de clase: "
                    #     + str(class_name)
                    #     + "    nombre de fichero:"
                    #     + str(file_name)
                    # )

                    gen_model.generate(
                        overwrite_model,
                        file_name,
                        class_name,
                        table.columns,
                        path_model,
                    )
                    gen_dao.generate(
                        overwrite_dao,
                        file_name,
                        class_name,
                        database_name,
                        database_class,
                        schema_file,
                        path_dao,
                    )

                    tables.append(file_name)

            if update_funtionalities:
                gen_fun.new_funtionalities(database_api, database_name, tables)

            return True

    except Exception as e:
        print("ERROR: Model generator -> generate: " + str(e))

    return False
