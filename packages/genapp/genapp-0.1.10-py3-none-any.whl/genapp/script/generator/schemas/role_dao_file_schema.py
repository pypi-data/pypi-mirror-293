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

    async def get_all_permissions(self) -> dict:
        result = {}
        try:
            async with self.database as db:
                query = select(
                    t_API_ROLE_PERMISSION_KEY.c.id_role,
                    t_API_ROLE_PERMISSION_KEY.c.id_permission,
                )
                query = query.order_by(
                    t_API_ROLE_PERMISSION_KEY.c.id_role,
                    t_API_ROLE_PERMISSION_KEY.c.id_permission,
                )

                query = await db.async_query(query)
                query = query.all()

                if query:
                    for id_role, id_permission in query:
                        id_role = int(id_role)
                        id_permission = int(id_permission)

                        if id_role not in result:
                            result[id_role] = []
                        result[id_role].append(id_permission)

        except Exception as e:
            print("ERROR: CLASS_NAME_KEYDao -> get_all_permissions: " + str(e))

        return result

    async def get_all_scopes(self) -> dict:

        try:
            async with self.database as db:
                query = select(
                    t_API_ROLE_SCOPE_KEY.c.id_role,
                    API_SCOPE_CLASS_KEY.name,
                    t_API_ROLE_SCOPE_KEY.c.value,
                )
                query = query.select_from(
                    t_API_ROLE_SCOPE_KEY.join(API_SCOPE_CLASS_KEY), API_SCOPE_CLASS_KEY
                )
                query = query.order_by(API_SCOPE_CLASS_KEY.name)

                result = await db.async_query(query)
                scope = result.all()

                data = {}  # Diccionario global
                if scope:
                    # Se prepara el diccionario interno
                    for id_role, key, value in scope:
                        # Si el id_role no está en el diccionario, agregarlo
                        if id_role not in data:
                            data[id_role] = {key: []}

                        # Si la clave no está en el diccionario interno, agregarla
                        if key not in data[id_role]:
                            data[id_role][key] = []

                        # Agregar el valor a la lista correspondiente
                        data[id_role][key].append(value)

                return data
        except Exception as e:
            print("ERROR: RoleDao -> get_all_scopes: " + str(e))

    # def getSomething(self, object : CLASS_NAME_KEYModel):
    #     results = []
    #     try:
    #         session = self.getSession()

    #         if session:
    #             # condition = and_(CLASS_NAME_KEY.attribute == object.key, CLASS_NAME_KEY.status == 0)
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
