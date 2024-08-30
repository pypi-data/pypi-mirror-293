from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.util import object as Obj
from app.util import string as St
from app.service.response.result import ResultAPI, ResultCodes
from app.service.request.request import Request

SET_OFFSET_LIMIT = "set_offset_limit"
CRUD_TYPE_QUERY = "query"


class Crud(Request):

    def __init__(self, database, crud_type, table, header, body):
        try:
            self.package = database
            self.crud_type = crud_type
            self.module = table
            self.header = header
            self.body = body

        except Exception as e:
            print("ERROR: CrudRequest -> init: " + str(e))
            self.return_server_error()

    async def start(self):
        pydantic = self._instance_pydantic()
        dao = self._instance_dao()

        offset, limit = self.get_offset_limit(self.body)

        if limit is not None and offset is not None:
            getattr(dao, SET_OFFSET_LIMIT)(offset, limit)

        if self.crud_type == CRUD_TYPE_QUERY:
            data, has_next = await getattr(dao, self.crud_type)(pydantic)
        else:
            data = await getattr(dao, self.crud_type)(pydantic)

        if isinstance(data, list):  # Resultado correcto de una query
            if data:
                return ResultAPI(has_next=has_next), data
            else:
                return ResultAPI(code=ResultCodes.NO_DATA), data

        if not data:
            return ResultAPI(code=ResultCodes.NO_DATA), data

        if not isinstance(data, Exception):  # Resultado sin errores
            return ResultAPI(code=ResultCodes.NO_MORE_DATA), data

        # Errores conocidos que se pueden dar al ejecutar el crud
        if isinstance(data, IntegrityError):
            self.response_error(description="Already registered")
        if isinstance(data, ProgrammingError):
            self.response_error(description="Not available")

        self.return_server_error()

    # Instancia un objecto pydantic
    def _instance_pydantic(self):
        try:
            return Obj.instance_model(
                self.package, self.module, self.crud_type, self.body
            )

        except ImportError as e:
            self.return_not_implemented()

        except ValidationError as e:
            # Si hay errores de validación, devuelve una respuesta de error con los detalles de la validación
            error_fields = [error["loc"][0] for error in e.errors()]
            error_message = f"Missing or invalid fields: '{', '.join(error_fields)}'"
            self.response_error(description=error_message)

        self.return_server_error()

    # Intancia un objecto DAO
    def _instance_dao(self):
        try:
            return Obj.instance_dao(self.package, self.module)

        except Exception as e:
            print("ERROR: Crud -> instance_dao: " + str(e))

        self.return_server_error()
