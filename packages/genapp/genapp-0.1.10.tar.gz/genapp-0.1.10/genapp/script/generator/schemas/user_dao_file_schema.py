from app.crud.dao import Dao
from app.crud.SCHEMA_KEY.SCHEMA_DATABASE_KEY import *
from app.DATABASE_KEY.DATABASE_NAME_KEY import DATABASE_CLASS_KEY
from fastapi.encoders import jsonable_encoder
from app.MODEL_KEY.DATABASE_NAME_KEY.FILE_NAME_KEY import CLASS_NAME_KEYModel
from sqlalchemy import and_, func, or_
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, joinedload, relationship


class CLASS_NAME_KEYDao(Dao):

    def __init__(self):
        self.database = DATABASE_CLASS_KEY()
        self.conn = self.database.newConn()

    async def login(self, object: CLASS_NAME_KEYModel):
        try:
            async with self.database as db:
                query = select(CLASS_NAME_KEY)
                conditions = and_(
                    CLASS_NAME_KEY.key == object.key,
                    CLASS_NAME_KEY.status == 0,
                    CLASS_NAME_KEY.username == object.username,
                )
                query = query.filter(and_(*conditions))

                result = await db.async_query(query)

                user = result.first()

                if user:
                    return int(user[0].id)

        except Exception as e:
            print("ERROR: CLASS_NAME_KEYDao -> login: " + str(e))

        return None

    async def get_user_by_email(self, object: CLASS_NAME_KEYModel):
        try:
            conditions = []
            conditions.append(CLASS_NAME_KEY.email == object.email)

            result, _ = await super().query(
                CLASS_NAME_KEY, conditions, output_format=self.SQLALCHEMY_OBJECT
            )

            return result[0] if result else None

        except Exception as e:
            print("ERROR: CLASS_NAME_KEYDao -> check_email: " + str(e))

        return None

    async def scope(self, object: CLASS_NAME_KEYModel):
        try:
            async with self.database as db:
                query = select(
                    t_API_USER_SCOPE_KEY.c.value,
                    API_SCOPE_CLASS_KEY.name,
                )
                query = query.select_from(
                    t_API_USER_SCOPE_KEY.join(API_SCOPE_CLASS_KEY)
                )
                query = query.where(t_API_USER_SCOPE_KEY.c.id_user == object.id)
                query = query.order_by(API_SCOPE_CLASS_KEY.name)

                result = await db.async_query(query)
                scope = self._format_scope(result.all())

                return scope

        except Exception as e:
            print("ERROR: CLASS_NAME_KEYDao -> scope: " + str(e))

    def _format_scope(self, scope):
        formatted_result = {}

        for value, name in scope:
            if name not in formatted_result:
                formatted_result[name] = []

            formatted_result[name].append(value)

        return formatted_result

    async def get_user_by_id(self, object: CLASS_NAME_KEYModel):
        try:
            async with self.database as db:

                query = select(CLASS_NAME_KEY)
                query = query.options(joinedload(CLASS_NAME_KEY.API_PERMISSION_KEY))
                query = query.filter(CLASS_NAME_KEY.id == object.id)

                user = await db.async_query(query)
                user = user.first()[0]

                if user:
                    if user.status == 0:
                        permissions = [
                            int(permission.id) for permission in user.API_PERMISSION_KEY
                        ]
                        # Actualizar el resultado con la lista de ID de permisos
                        return user, permissions

        except Exception as e:
            print("ERROR: ApiUsuariosDao -> get_user_by_id: " + str(e))

        return None, None

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
