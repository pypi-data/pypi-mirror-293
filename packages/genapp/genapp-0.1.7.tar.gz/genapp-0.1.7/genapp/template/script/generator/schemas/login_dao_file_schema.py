from app.crud.dao import Dao
from app.crud.SCHEMA_KEY.SCHEMA_DATABASE_KEY import *
from app.DATABASE_KEY.DATABASE_NAME_KEY import DATABASE_CLASS_KEY
from fastapi.encoders import jsonable_encoder
from app.MODEL_KEY.DATABASE_NAME_KEY.API_LOGIN_KEY import API_LOGIN_CLASS_KEYModel
from sqlalchemy import and_, or_
from sqlalchemy.future import select


class API_LOGIN_CLASS_KEYDao(Dao):
    def __init__(self):
        self.database = DATABASE_CLASS_KEY()
        self.conn = self.database.newConn()

    async def last_logins(self, elementPydantic, timestamp):
        try:
            select = []
            select.append(API_LOGIN_CLASS_KEY.key)
            select.append(API_LOGIN_CLASS_KEY.timestamp)
            select.append(API_LOGIN_CLASS_KEY.is_bot)
            select.append(API_LOGIN_CLASS_KEY.status)
            conditions = self._getCondition(elementPydantic)
            conditions.append(API_LOGIN_CLASS_KEY.timestamp >= timestamp)

            return await super().query(API_LOGIN_CLASS_KEY, conditions, select)

        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_LOGIN_CLASS_KEYDao -> last_logins: "
                + str(e)
            )

        return None, None

    async def last_distinct_logins(self, object, timestamp):
        try:
            select = []
            distinct = []
            select.append(API_LOGIN_CLASS_KEY.key)
            select.append(API_LOGIN_CLASS_KEY.timestamp)
            select.append(API_LOGIN_CLASS_KEY.is_bot)
            select.append(API_LOGIN_CLASS_KEY.status)
            distinct.append(API_LOGIN_CLASS_KEY.key)
            conditions = self._getCondition(object)
            conditions.append(API_LOGIN_CLASS_KEY.timestamp >= timestamp)

            return await super().query(
                API_LOGIN_CLASS_KEY, conditions, select, distinct
            )

        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_LOGIN_CLASS_KEYDao -> last_distinct_logins: "
                + str(e)
            )

        return None, None

    # async def getSomething(self, elementPydantic, date_init, date_end):
    #     try:
    #         select = []

    #         select.append(API_LOGIN_CLASS_KEY.attribute1)
    #         select.append(API_LOGIN_CLASS_KEY.attribute2)
    #         # select.append(API_LOGIN_CLASS_KEY.attribute3)
    #         select.append(API_LOGIN_CLASS_KEY.attribute4)

    #         conditions = self._getCondition(elementPydantic)
    #         conditions.append(API_LOGIN_CLASS_KEY.date.between(date_init, date_end))
    #         conditions.append(API_LOGIN_CLASS_KEY.attribute1 == 100)

    #         return await super().query(API_LOGIN_CLASS_KEY, conditions, select)

    #     except Exception as e:
    #         print(f"ERROR: DATABASE_CLASS_KEY API_LOGIN_CLASS_KEYDao -> getSomething: " + str(e))
    #         return e, None

    def _getCondition(self, elementPydantic):
        try:
            conditions = []
            for attribute_name, attribute_value in elementPydantic.__dict__.items():
                if attribute_value is not None:
                    sqlalchemy_condition = (
                        getattr(API_LOGIN_CLASS_KEY, attribute_name) == attribute_value
                    )
                    conditions.append(sqlalchemy_condition)
            if conditions:
                return conditions
            else:
                return None

        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_LOGIN_CLASS_KEYDao -> getCondition: "
                + str(e)
            )
        return None

    def _initObjectSQLAlchemy(self, elementPydantic):
        try:
            attributes = elementPydantic.model_dump(
                exclude_none=True, exclude_unset=True
            )
            return API_LOGIN_CLASS_KEY(**attributes)
        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_LOGIN_CLASS_KEYDao -> initObjectSQLAlchemy: "
                + str(e)
            )
        return None

    async def query(self, elementPydantic, output_format=None):
        conditions = self._getCondition(elementPydantic)
        return await super().query(
            API_LOGIN_CLASS_KEY, conditions, output_format=output_format
        )

    async def insert(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().insert(element)

    async def update(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().update(element)

    async def delete(self, elementPydantic):
        element = self._initObjectSQLAlchemy(elementPydantic)
        return await super().delete(element)
