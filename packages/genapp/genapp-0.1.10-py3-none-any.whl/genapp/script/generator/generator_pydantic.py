
from sqlalchemy import (
    PrimaryKeyConstraint,
    UniqueConstraint,
    types,
)
from sqlalchemy.dialects.mssql import *

from genapp.script.util import file as Fl
from genapp.script.util import string as St



###########################################################
###################### Pydantic model #####################
###########################################################
def generate(overwrite, file_name, class_name, columns, path):
    try:
        imports = set()
        imports.add("from pydantic import BaseModel")
        imports.add("from typing import Optional")
        imports.add("from datetime import datetime, time")

        content = ""

        content += generate_generic_class(class_name, columns)
        content += generate_insert_class(class_name, columns)
        content += generate_update_class(class_name, columns)
        content += generate_delete_class(class_name, columns)

        if imports:
            content = "\n".join(sorted(imports)) + "\n\n" + content

        if overwrite or not Fl.exist_file(path, file_name):
            Fl.new_file(path, file_name, content)

    except Exception as e:
        print("ERROR: Generator pydantic -> generate_pydantic_model_file: " + str(e))


def generate_update_class(class_name, columns):
    try:
        content = f"\nclass {class_name}UpdateModel(BaseModel):\n"

        for column in columns:
            data_type = detect_pydantic_type(column.type)
            is_primary = any(
                isinstance(
                    c, PrimaryKeyConstraint) and column.name in c.columns
                for c in column.table.constraints
            )
            column_name = St.text_to_snake(str(column.name))
            column_name = St.get_valid_attribute(column_name)
            if is_primary:
                content += f"    {column_name}: {data_type}\n"
            else:
                # Usar una cadena Unicode para representar el nombre de la columna
                content += f"    {column_name}: Optional[{data_type}] = None\n"

        return content

    except Exception as e:
        print("ERROR: Generator pydantic -> generate_update_class: " + str(e))


def generate_insert_class(class_name, columns):
    try:
        content = f"\nclass {class_name}InsertModel(BaseModel):\n"

        for column in columns:
            data_type = detect_pydantic_type(column.type)
            is_unique = any(
                isinstance(c, UniqueConstraint) and set(c.columns) == {column}
                for c in column.table.constraints
            )
            is_unique = is_unique or any(
                i.unique and set(i.columns) == {column} for i in column.table.indexes
            )
            is_primary = any(
                isinstance(
                    c, PrimaryKeyConstraint) and column.name in c.columns
                for c in column.table.constraints
            )

            column_name = St.text_to_snake(str(column.name))
            column_name = St.get_valid_attribute(column_name)
            if is_unique or is_primary or not column.nullable:
                content += f"    {column_name}: {data_type}\n"
            else:
                content += f"    {column_name}: Optional[{data_type}] = None\n"

        return content

    except Exception as e:
        print("ERROR: Generator pydantic -> generate_insert_class: " + str(e))


def generate_generic_class(class_name, columns):
    try:
        content = f"\nclass {class_name}Model(BaseModel):\n"

        for column in columns:
            data_type = detect_pydantic_type(column.type)
            column_name = St.text_to_snake(str(column.name))
            column_name = St.get_valid_attribute(column_name)
            content += f"    {column_name}: Optional[{data_type}] = None\n"

        return content

    except Exception as e:
        print("ERROR: Generator pydantic -> generate_query_class: " + str(e))


def generate_delete_class(class_name, columns):
    try:
        content = f"\nclass {class_name}DeleteModel(BaseModel):\n"

        for column in columns:
            data_type = detect_pydantic_type(column.type)
            is_primary = any(
                isinstance(
                    c, PrimaryKeyConstraint) and column.name in c.columns
                for c in column.table.constraints
            )

            column_name = St.text_to_snake(str(column.name))
            column_name = St.get_valid_attribute(column_name)

            if is_primary:
                content += f"    {column_name}: {data_type}\n"

        return content
    except Exception as e:
        print("ERROR: Generator pydantic -> generate_delete_class: " + str(e))


def detect_pydantic_type(column_type):
    try:
        if (
            isinstance(column_type, types.Float)
            or isinstance(column_type, types.Numeric)
            or isinstance(column_type, types.REAL)
        ):
            return "float"  # if is_nullable else 'float'
        elif (
            isinstance(column_type, types.Integer)
            or isinstance(column_type, types.SmallInteger)
            or isinstance(column_type, types.BigInteger)
        ):
            return "int"  # if is_nullable else 'int'
        elif (
            isinstance(column_type, types.DATETIME)
            or isinstance(column_type, types.TIMESTAMP)
            or isinstance(column_type, types.DATE)
            or isinstance(column_type, SMALLDATETIME)
        ):
            return "datetime"  # if is_nullable else 'datetime'
        elif (
            isinstance(column_type, types.String)
            or isinstance(column_type, types.Unicode)
            or isinstance(column_type, types.Text)
        ):
            return "str"  # if is_nullable else 'str'
        elif (
            isinstance(column_type, types.Boolean)
            or isinstance(column_type, types.BINARY)
            or isinstance(column_type, BIT)
        ):
            return "bool"  # if is_nullable else 'bool'
        elif isinstance(column_type, VARBINARY) or isinstance(column_type, IMAGE):
            return "bytes"  # if is_nullable else 'bytes'
        elif isinstance(column_type, types.JSON):
            return "dict"  # if is_nullable else 'dict'
        elif isinstance(column_type, types.ARRAY):
            return "list"  # if is_nullable else 'list'
        else:
            return f"{column_type.python_type.__name__}"

    except Exception as e:
        print("ERROR: Generator pydantic -> detect_pydantic_type: " + str(e))

    return None
