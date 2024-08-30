from app.crud.dao import Dao
from app.crud.SCHEMA_KEY.SCHEMA_DATABASE_KEY import *
from app.DATABASE_KEY.DATABASE_NAME_KEY import DATABASE_CLASS_KEY
from fastapi.encoders import jsonable_encoder
from app.MODEL_KEY.DATABASE_NAME_KEY.API_CONNECTION_KEY import (
    API_CONNECTION_CLASS_KEYModel,
)
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.sql import func


class API_CONNECTION_CLASS_KEYDao(Dao):
    def __init__(self):
        self.database = DATABASE_CLASS_KEY()
        self.conn = self.database.newConn()

    async def get_last_connections(self, timestamp_delta):
        try:
            async with self.database as db:
                subquery = (
                    select(
                        API_CONNECTION_CLASS_KEY.ip,
                        API_CONNECTION_CLASS_KEY.block,
                        API_CONNECTION_CLASS_KEY.id,
                        API_CONNECTION_CLASS_KEY.country_code,
                        func.row_number()
                        .over(
                            partition_by=API_CONNECTION_CLASS_KEY.ip,
                            order_by=API_CONNECTION_CLASS_KEY.timestamp.desc(),
                        )
                        .label("rn"),
                    )
                    .where(API_CONNECTION_CLASS_KEY.timestamp > timestamp_delta)
                    .alias("subquery")
                )

                stmt = select(
                    subquery.c.ip,
                    subquery.c.block,
                    subquery.c.id,
                    subquery.c.country_code,
                ).where(subquery.c.rn == 1)

                query = await db.async_query(stmt)
                query = query.all()

                if query:
                    return self.format_data(query)

        except Exception as e:
            print(
                f"ERROR: GenericAppDB API_CONNECTION_CLASS_KEYDao -> get_last_connections: "
                + str(e)
            )

        return None

    def format_data(self, data):
        try:
            return {tuple[0]: (tuple[1], tuple[2], tuple[3]) for tuple in data}

        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_CONNECTION_CLASS_KEYDao -> format_data: "
                + str(e)
            )

        return None

    # async def getSomething(self, elementPydantic, date_init, date_end):
    #     try:
    #         select = []

    #         select.append(API_CONNECTION_CLASS_KEY.attribute1)
    #         select.append(API_CONNECTION_CLASS_KEY.attribute2)
    #         # select.append(API_CONNECTION_CLASS_KEY.attribute3)
    #         select.append(API_CONNECTION_CLASS_KEY.attribute4)

    #         conditions = self._getCondition(elementPydantic)
    #         conditions.append(API_CONNECTION_CLASS_KEY.date.between(date_init, date_end))
    #         conditions.append(API_CONNECTION_CLASS_KEY.attribute1 == 100)

    #         return await super().query(API_CONNECTION_CLASS_KEY, conditions, select)

    #     except Exception as e:
    #         print(f"ERROR: DATABASE_CLASS_KEY API_CONNECTION_CLASS_KEYDao -> getSomething: " + str(e))
    #         return e

    def _getCondition(self, elementPydantic):
        try:
            conditions = []
            for attribute_name, attribute_value in elementPydantic.__dict__.items():
                if attribute_value is not None:
                    sqlalchemy_condition = (
                        getattr(API_CONNECTION_CLASS_KEY, attribute_name)
                        == attribute_value
                    )
                    conditions.append(sqlalchemy_condition)
            if conditions:
                return conditions
            else:
                return None

        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_CONNECTION_CLASS_KEYDao -> getCondition: "
                + str(e)
            )
        return None

    def _initObjectSQLAlchemy(self, elementPydantic):
        try:
            attributes = elementPydantic.model_dump(
                exclude_none=True, exclude_unset=True
            )
            return API_CONNECTION_CLASS_KEY(**attributes)
        except Exception as e:
            print(
                f"ERROR: DATABASE_CLASS_KEY API_CONNECTION_CLASS_KEYDao -> initObjectSQLAlchemy: "
                + str(e)
            )
        return None

    async def query(self, elementPydantic, output_format=None):
        conditions = self._getCondition(elementPydantic)
        return await super().query(
            API_CONNECTION_CLASS_KEY, conditions, output_format=output_format
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
