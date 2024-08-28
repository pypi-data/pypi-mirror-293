import os

from app.util import file as Fl
from app.util import string as St

from . import constants as c

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.dirname(THIS_PATH)
ROOT_PATH = os.path.dirname(SCRIPT_PATH)
APP_PATH = os.path.join(ROOT_PATH, f"{c.APP}")


###########################################################
###################### Funtionalities #####################
###########################################################


def new_funtionalities(database_api, database_name, tables):
    try:
        funtionalities = []
        if tables and database_api and database_name:
            for table in tables:
                file_name = St.text_to_snake(table)
                class_name = St.text_to_class(table)
                for crud in c.CRUDS:
                    id = funtionality_in_db(
                        database_api, crud, database_name, file_name
                    )
                    if id:
                        funtionality = (class_name, file_name, crud, id)
                        funtionalities.append(funtionality)
            # generate_map_funtionality(database_name, funtionalities)

    except Exception as e:
        print("ERROR: Generator funtionalities -> new_funtionalities: " + str(e))


def funtionality_in_db(database_api, crud_type, database_name, file_name):
    try:
        if database_api:
            query = f"SELECT * \
                        FROM {c.API_FUNTIONALITY} \
                        WHERE \"segment_1\" = 'crud' \
                            AND \"segment_4\" = '{file_name}' \
                            AND \"segment_3\" = '{crud_type}' \
                            AND \"segment_2\" = '{database_name}'"

            # query = f"SELECT * \
            #             FROM {c.API_FUNTIONALITY} \
            #             WHERE \"SEGMENT_1\" = 'crud' \
            #                 AND \"SEGMENT_4\" = '{file_name}' \
            #                 AND \"SEGMENT_3\" = '{crud_type}' \
            #                 AND \"SEGMENT_2\" = '{database_name}'"

            exists = database_api.query_no_orm(query)

            if not exists:
                # insert = f'INSERT INTO {c.API_FUNTIONALITY}\
                #             ("SEGMENT_1", "SEGMENT_4", "SEGMENT_2", "SEGMENT_3", "STATUS")\
                #             VALUES(\'crud\',\'{file_name}\',\'{database_name}\',\'{crud_type}\', 1)'

                insert = f'INSERT INTO {c.API_FUNTIONALITY}\
                            ("segment_1", "segment_4", "segment_2", "segment_3", "status")\
                            VALUES(\'crud\',\'{file_name}\',\'{database_name}\',\'{crud_type}\', 1)'

                database_api.execute_no_orm(insert)
                result = database_api.query_no_orm(query)
                if result:
                    return result[0].get(c.API_FUNTIONALITY_ATT_ID)
            else:
                return exists[0].get(c.API_FUNTIONALITY_ATT_ID)

    except Exception as e:
        print("ERROR: Generator funtionalities -> funtionality_in_db: " + str(e))

    return None


# def generate_map_funtionality(database_name, funtionalities):
#     try:
#         if funtionalities:
#             # Para los imports

#             lines = []
#             for funtionality in funtionalities:
#                 class_name, file_name, crud, id = funtionality

#                 new_row_import = f"from {c.CRUD}.{database_name}.{file_name}_dao import {class_name}Dao\n"

#                 if new_row_import not in lines:
#                     lines.append(new_row_import)

#             # Se inicia el mapa de funciones
#             lines.append("\REQUEST = {\n")

#             # Para el contenido del mapa de funciones
#             for funtionality in funtionalities:
#                 class_name, file_name, crud, id = funtionality

#                 new_row_map = f"    {id} : {class_name}Dao.{crud},\n"

#                 if new_row_map not in lines:
#                     lines.append(new_row_map)

#             # Se cierra el mapa de funciones
#             lines.append("\n}\n")

#             path_service = os.path.join(APP_PATH, c.SERVICE)
#             path_out = os.path.join(path_service, c.ROUTES)

#             Fl.new_directory(path_out)
#             Fl.write_lines(path_out, c.FILE_NAME_MAP_CRUD, lines)

#     except Exception as e:
#         print("ERROR: Generator funtionalities -> generate_map_funtionality: " + str(e))

#     return None
