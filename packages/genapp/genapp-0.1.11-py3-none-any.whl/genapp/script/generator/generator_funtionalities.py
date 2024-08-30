import os
from genapp.script.util import string as St

from . import constants as c

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

    except Exception as e:
        print("ERROR: Generator funtionalities -> new_funtionalities: " + str(e))


def funtionality_in_db(database_api, crud_type, database_name, file_name):
    try:
        if database_api:
            api_funtionality = os.getenv("API_FUNTIONALITY")
            query = f"SELECT * \
                        FROM {api_funtionality} \
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

                insert = f'INSERT INTO {api_funtionality}\
                            ("segment_1", "segment_4", "segment_2", "segment_3", "status")\
                            VALUES(\'crud\',\'{file_name}\',\'{database_name}\',\'{crud_type}\', 1)'

                database_api.execute_no_orm(insert)
                result = database_api.query_no_orm(query)
                if result:
                    return result[0].get(os.getenv("API_FUNTIONALITY_ATT_ID"))
            else:
                return exists[0].get(os.getenv("API_FUNTIONALITY_ATT_ID"))

    except Exception as e:
        print("ERROR: Generator funtionalities -> funtionality_in_db: " + str(e))

    return None

