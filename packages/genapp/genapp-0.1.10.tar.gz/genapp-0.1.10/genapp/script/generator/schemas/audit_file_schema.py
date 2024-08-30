from app.CRUD_KEY.DATABASE_NAME_KEY.API_AUDIT_REQUEST_KEY_dao import (
    API_AUDIT_REQUEST_CLASS_KEYDao,
)
from app.CRUD_KEY.DATABASE_NAME_KEY.API_AUDIT_REQUEST_NOT_LOGGED_KEY_dao import (
    API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEYDao,
)
from app.CRUD_KEY.DATABASE_NAME_KEY.API_AUDIT_RESPONSE_KEY_dao import (
    API_AUDIT_RESPONSE_CLASS_KEYDao,
)
from app.MODEL_KEY.DATABASE_NAME_KEY.API_AUDIT_REQUEST_KEY import (
    API_AUDIT_REQUEST_CLASS_KEYModel,
)
from app.MODEL_KEY.DATABASE_NAME_KEY.API_AUDIT_REQUEST_NOT_LOGGED_KEY import (
    API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEYModel,
)
from app.MODEL_KEY.DATABASE_NAME_KEY.API_AUDIT_RESPONSE_KEY import (
    API_AUDIT_RESPONSE_CLASS_KEYModel,
)
from app.util import date as Dt
from app.util import request as Rq


class Audit:

    async def save_audit(
        request,
        id_login,
        request_content,
        response_result,
        timestamp_init,
        timestamp_end,
    ):
        # Enqueue la auditoría de solicitud sin esperar
        id_request = await Audit._audit_request(
            request, id_login, request_content, timestamp_init
        )
        # Enqueue la auditoría de respuesta sin esperar
        await Audit._audit_response(id_request, response_result, timestamp_end)

    async def audit_request_not_logged(request, id_conn, timestamp):
        try:
            url = Rq.get_url(request, complete=True)
            params = Rq.get_params(request)
            headers = Rq.get_clean_headers(request)

            dto = AuditRequestNotLoggedModel(
                id_conn=id_conn,
                body=headers,
                params=params,
                timestamp=timestamp,
                url=url,
            )
            await AuditRequestNotLoggedDao().insert(dto)

        except Exception as e:
            print("ERROR: Audit -> audit_request_not_logged: " + str(e))

    async def _audit_request(
        request,
        id_login,
        request_content,
        timestamp_init,
    ):
        try:
            url = Rq.get_url(request)
            dto = API_AUDIT_REQUEST_CLASS_KEYModel(
                id_login=id_login,
                request=request_content,
                timestamp=timestamp_init,
                url=url,
            )
            audit_request = await API_AUDIT_REQUEST_CLASS_KEYDao().insert(dto)

            if audit_request:
                return audit_request.id

        except Exception as e:
            print("ERROR: Audit -> audit_request: " + str(e))

    async def _audit_response(id_request, response_result, timestamp_end):
        try:
            dto = API_AUDIT_RESPONSE_CLASS_KEYModel(
                response=response_result,
                timestamp=timestamp_end,
                id_request=id_request,
            )

            return await API_AUDIT_RESPONSE_CLASS_KEYDao().insert(dto)
        except Exception as e:
            print("ERROR: Audit -> audit_response: " + str(e))
