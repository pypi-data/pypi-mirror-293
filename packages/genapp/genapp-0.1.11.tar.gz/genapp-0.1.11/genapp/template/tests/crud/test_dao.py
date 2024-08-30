import re
import pytest
from time import sleep
from app.crud.dao import Dao
from app.util import object as Obj
from app.util import path as Path
from app.util import string as St


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dao_data",
    Path.get_files_info(
        Path.get_path_absolute("app/crud"),
        exclude_subdirectories=[
            "schema",
        ],  # "avre", "mere", "delfos", "tarsys"],
    ),
    ids=lambda dao_data: f"{dao_data.get('package')}_{re.sub(r'_dao$', '', dao_data.get('name'))}",
)
async def test_dao_query(dao_data):
    package = dao_data.get("package", None)

    if package != ".":
        dao_file_name = dao_data.get("name", None)

        model_name = re.sub(r"_dao$", "", dao_file_name)

        pydantic = Obj.instance_model(
            package=package, name=model_name, crud_type="query"
        )

        dao = Obj.instance_object(
            directory_list=[Obj.CRUD_PATH], name=dao_file_name, package=package
        )

        # print("pydantic:", pydantic, "   dao:", dao)

        dao.set_offset_limit(0, 1)
        data, has_next = await dao.query(pydantic)
        assert isinstance(data, list)  # Asegura que data sea una lista
        # Asegura que has_next sea un booleano
        assert isinstance(has_next, bool)


# Aquí puedes agregar más aserciones para validar otros aspectos de los resultados
