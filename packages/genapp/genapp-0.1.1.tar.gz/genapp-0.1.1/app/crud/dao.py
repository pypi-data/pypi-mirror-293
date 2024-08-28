from time import sleep

from fastapi.encoders import jsonable_encoder
from sqlalchemy import (
    Column,
    Integer,
    String,
    and_,
    column,
    create_engine,
    insert,
    inspect,
    literal_column,
    or_,
    text,
    update,
    desc,
    asc,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select


class Dao:
    # Query format output
    TYPE_CONDITION_AND = "AND"
    TYPE_CONDITION_OR = "OR"
    CONDITIONATED = "CONDITIONATED"
    SQLALCHEMY_OBJECT = 1
    JSON = 2

    # Order by types
    DESC = "desc"
    ASC = "asc"

    MAX_ROWS = 1000
    MAX_ROWS_FRACTIONAL_QUERY = 20

    database = None
    conn = None

    limit = None
    offset = None

    async def query(
        self,
        table,
        conditions,
        select_elements=None,
        select_from=None,
        group_by=None,
        distinct_elements=None,
        order_by=None,  # (ATTRIBUTE, [ASC | DESC])
        output_format=None,
        type_condition=None,
    ):
        try:
            async with self.database as db:
                query = self._build_query(
                    table,
                    conditions,
                    type_condition,
                    select_elements,
                    select_from,
                    distinct_elements,
                    group_by,
                )
                has_next = False

                if order_by is not None:
                    query = self._apply_order_by(query, order_by)

                if self.limit is not None and self.offset is not None:
                    query, has_next = await self._apply_pagination_and_order(
                        query, db, table, select_elements, order_by
                    )
                else:
                    query = query.limit(self.MAX_ROWS)
                result = await db.async_query(query)
                rows = result.all()

                data = self._format_output(rows, table, select_elements, output_format)

                return data, has_next
        except Exception as e:
            print("ERROR: Dao -> query:", str(e))
            return str(e), False

    def _build_query(
        self,
        table,
        conditions,
        type_condition,
        select_elements,
        select_from,
        distinct_elements,
        group_by,
    ):
        if isinstance(table, list):
            query = select(*table)
        else:
            query = select(table)

        if select_elements:
            query = query.with_only_columns(*select_elements)

        if select_from:
            query = query.select_from(*select_from)

        if distinct_elements:
            query = query.distinct(*distinct_elements)

        if conditions is not None:
            if type_condition:
                if type_condition == self.CONDITIONATED:
                    query = query.filter(conditions)

                elif type_condition == self.TYPE_CONDITION_OR:
                    query = query.filter(or_(*conditions))

            else:
                query = query.filter(and_(*conditions))

        if group_by:
            query = query.group_by(*group_by)

        return query

    async def _apply_pagination_and_order(
        self, query, db, table, select_elements, order_by
    ):
        query = query.limit(self.limit).offset(self.offset)

        if db.mandatory_order and order_by is None:
            query = self._apply_mandatory_order_by(query, table, select_elements)

        next_offset = self.offset + self.limit + 1
        query_next = query.limit(1).offset(next_offset)
        result = await db.async_query(query_next)
        rows = result.all()
        has_next = bool(rows)

        return query, has_next

    def _apply_order_by(self, query, order_by):
        attribute, odr = order_by
        if odr == self.DESC:
            return query.order_by(desc(attribute))
        elif odr == self.ASC:
            return query.order_by(asc(attribute))

    def _apply_mandatory_order_by(self, query, table, select_elements):
        if not select_elements:
            primary_key = self._get_primary_key(table)
            query = query.order_by(primary_key)
        else:
            query = query.order_by(*select_elements)

        return query

    def _format_output(self, rows, table, select_elements, output_format):
        if output_format == self.SQLALCHEMY_OBJECT:
            return [row[0] for row in rows]
        else:
            if isinstance(table, list):
                select_elements = table

            if select_elements:
                columns = [column.key for column in select_elements]
                return [
                    {column: getattr(row, column) for column in columns} for row in rows
                ]
            else:
                return [jsonable_encoder(row[0]) for row in rows]

    async def insert(self, element):
        try:
            async with self.database as db:
                return await db.async_insert(element)

        except Exception as e:
            print("ERROR: Dao -> insert: " + str(e))
            return e

    async def update(self, element):
        try:
            async with self.database as db:
                return await db.async_merge(element)

        except Exception as e:
            print("ERROR: Dao -> update: " + str(e))
            return e

    async def get(self, element, ident=None):
        try:

            async with self.database as db:
                class_name = (
                    element.__class__
                )  # Devuelve que el nombre del tipo de objeto (Tabla en BBDD)
                if not ident:
                    mapper = inspect(class_name)
                    primary_key_name = mapper.primary_key[0].name
                    ident = getattr(element, primary_key_name)
                return await db.async_get(class_name, ident)

        except Exception as e:
            print("ERROR: Dao -> get: " + str(e))
            return e

    async def delete(self, element, ident=None):
        try:
            element_exists = await self.get(element, ident)
            async with self.database as db:
                if element_exists:
                    return await db.async_delete(element_exists)
                else:
                    return False
        except Exception as e:
            print("ERROR: Dao -> delete: " + str(e))
            return e

    async def exists(self, element, match_columns):
        try:
            async with self.database as db:
                filter_conditions = {
                    column.name: getattr(element, column.name)
                    for column in match_columns
                }
                stmt = select(element.__class__).filter_by(**filter_conditions)

                result = await db.async_query(stmt)
                element_exists = result.first()

                return True if element_exists else False

        except Exception as e:
            print("ERROR: Dao -> exists: " + str(e))
            return e

    async def get_or_insert(self, element, match_columns):
        try:
            async with self.database as db:
                filter_conditions = {
                    column.name: getattr(element, column.name)
                    for column in match_columns
                }
                stmt = select(element.__class__).filter_by(**filter_conditions)

                result = await db.async_query(stmt)
                result = result.first()

                if result:
                    element_exists = result[0]
                    return element_exists

                return await db.async_insert(element)

        except Exception as e:
            print("ERROR: Dao -> get_or_insert: " + str(e))
            return e

    def set_offset_limit(self, offset, limit):
        self.limit = limit
        self.offset = offset

    def _get_primary_key(self, table):
        try:
            mapper = inspect(table)
            return mapper.primary_key[0]
        except Exception as e:
            print("ERROR: Dao -> get_primary_key: " + str(e))
            return e

    # Dada una lista de tuplas obtenidas de una tabla donde cada elemento de
    # la tupla representa en posicion un atributo de la consulta, asigna la key correspondiente al valor
    def _encode_data(self, table, list) -> dict:
        try:
            if list:
                att_class = [name for name in table.__dict__.keys()]
                columns = [name for name in att_class if not name.startswith("_")]
                processed_data = []
                for item in list:

                    json_data = {}
                    for key, value in zip(columns, item):
                        json_data[key] = value

                    processed_data.append(json_data)

                return jsonable_encoder(processed_data)

        except Exception as e:
            print("ERROR: Dao -> encode_data: " + str(e))
            return e
