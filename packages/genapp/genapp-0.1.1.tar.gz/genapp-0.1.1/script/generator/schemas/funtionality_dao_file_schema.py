from app.crud.dao import Dao
from app.crud.SCHEMA_KEY.SCHEMA_DATABASE_KEY import *
from app.DATABASE_KEY.DATABASE_NAME_KEY import DATABASE_CLASS_KEY
from fastapi.encoders import jsonable_encoder
from app.MODEL_KEY.DATABASE_NAME_KEY.FILE_NAME_KEY import CLASS_NAME_KEYModel
from sqlalchemy import and_, or_
from sqlalchemy.future import select


class CLASS_NAME_KEYDao(Dao):
    def __init__(self):
        self.database = DATABASE_CLASS_KEY()
        self.conn = self.database.newConn()

    async def get_no_auth_funtionalities(self):
        try:
            conditions = []
            conditions.append(CLASS_NAME_KEY.auth == 0)
            conditions.append(CLASS_NAME_KEY.status == 1)

            data, _ = await super().query(CLASS_NAME_KEY, conditions)

            return data

        except Exception as e:
            print(
                f"ERROR: GenericAppDB CLASS_NAME_KEYDao -> get_no_auth_funtionalities: "
                + str(e)
            )

        return None

    async def get_all_permissions(self) -> dict:
        result = {}
        try:
            async with self.database as db:
                query = select(
                    t_API_FUNTIONALITY_PERMISSION_KEY.c.id_funtionality,
                    t_API_FUNTIONALITY_PERMISSION_KEY.c.id_permission,
                )
                query = query.order_by(
                    t_API_FUNTIONALITY_PERMISSION_KEY.c.id_funtionality,
                    t_API_FUNTIONALITY_PERMISSION_KEY.c.id_permission,
                )

                query = await db.async_query(query)
                permissions = query.all()

                if permissions:
                    for id_funtionality, id_permission in permissions:
                        id_funtionality = int(id_funtionality)
                        id_permission = int(id_permission)
                        if id_funtionality not in result:
                            result[id_funtionality] = []
                        result[id_funtionality].append(id_permission)

        except Exception as e:
            print("ERROR: CLASS_NAME_KEYDao -> get_all_permissions: " + str(e))

        return result

    async def get_all_funtionalities(self) -> dict:
        result = {}
        try:
            async with self.database as db:
                query = select(CLASS_NAME_KEY)
                query = query.filter(and_(CLASS_NAME_KEY.status == 1))

                query = await db.async_query(query)
                query = query.all()

                if query:
                    for row in query:
                        row = row[0]
                        # Sustituir aqui el nombre de los atributos en bbdd en caso que sea necesario
                        segment_1 = row.segment_1
                        segment_2 = row.segment_2
                        segment_3 = row.segment_3
                        segment_4 = row.segment_4

                        if segment_1 not in result:
                            result[segment_1] = {}

                        if segment_2 is not None:
                            if segment_2 not in result[segment_1]:
                                result[segment_1][segment_2] = {}

                            if segment_3 is not None:
                                if segment_3 not in result[segment_1][segment_2]:
                                    result[segment_1][segment_2][segment_3] = {}

                                if segment_4 is not None:
                                    result[segment_1][segment_2][segment_3][
                                        segment_4
                                    ] = row
                                else:
                                    result[segment_1][segment_2][segment_3] = row
                            else:
                                result[segment_1][segment_2] = row
                        else:
                            result[segment_1] = row

        except Exception as e:
            print("ERROR: CLASS_NAME_KEYDao -> get_all_funtionalities: " + str(e))

        return result

    # def getSomething(self, object : CLASS_NAME_KEYModel):
    #     results = []
    #     try:
    #         session = self.getSession()

    #         if session:
    #             # condition = and_(CLASS_NAME_KEY.attribute == object.clave, CLASS_NAME_KEY.status == 0)
    #             # result = session.query(CLASS_NAME_KEY).filter(condition).scalar()
    #             result = session.query(CLASS_NAME_KEY).get(object.id)

    #             if result:
    #                 return result.some_attribute

    #             # return True if result else False

    #     except Exception as e:
    #         print("ERROR: CLASS_NAME_KEYDao -> getSomething: " + str(e))

    #     finally:
    #         session.close()

    #     return results

    def _initObjectSQLAlchemy(self, elementPydantic):
        try:
            attributes = elementPydantic.model_dump(
                exclude_none=True, exclude_unset=True
            )
            return CLASS_NAME_KEY(**attributes)
        except Exception as e:
            print(f"ERROR: CLASS_NAME_KEYDao -> initObjectSQLAlchemy: " + str(e))
        return None

    def _getCondition(self, element_pydantic):
        try:
            conditions = []
            for attribute_name, attribute_value in element_pydantic.__dict__.items():
                if attribute_value is not None:
                    sqlalchemy_condition = (
                        getattr(CLASS_NAME_KEY, attribute_name) == attribute_value
                    )
                    conditions.append(sqlalchemy_condition)
            if conditions:
                return conditions
            else:
                return None

        except Exception as e:
            print(f"ERROR: CLASS_NAME_KEYDao -> getCondition: " + str(e))
        return None

    async def query(self, element_pydantic, output_format=None):
        conditions = self._getCondition(element_pydantic)
        return await super().query(
            CLASS_NAME_KEY, conditions, output_format=output_format
        )

    async def update(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().update(element)

    async def delete(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().delete(element)

    async def insert(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().insert(element)
