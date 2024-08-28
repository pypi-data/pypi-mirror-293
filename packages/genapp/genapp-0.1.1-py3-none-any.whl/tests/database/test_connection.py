import os

from sqlalchemy import text

from app.database.genericapp import GenericAppDB


def test_connection_no_orm_genericapp():
    try:
        database = GenericAppDB()
        database.connect()
        cursor = database.connection.cursor()

        assert cursor is not None
    except Exception as e:
        assert False


async def test_connection_sqlalchemy_genericapp():
    try:
        database = GenericAppDB()

        async with database as db:
            result = await db.async_query(text("SELECT version();"))
            print(result)
            assert not isinstance(result, Exception) and result is not None
    except Exception as e:
        assert False
