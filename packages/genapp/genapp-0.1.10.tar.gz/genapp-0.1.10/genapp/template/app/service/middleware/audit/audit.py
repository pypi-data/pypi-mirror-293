from app.crud.genericapp.audit_request_dao import (
    AuditRequestDao,
)
from app.crud.genericapp.audit_request_not_logged_dao import (
    AuditRequestNotLoggedDao,
)
from app.crud.genericapp.audit_response_dao import (
    AuditResponseDao,
)
from app.model.genericapp.audit_request import (
    AuditRequestModel,
)
from app.model.genericapp.audit_request_not_logged import (
    AuditRequestNotLoggedModel,
)
from app.model.genericapp.audit_response import (
    AuditResponseModel,
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
            dto = AuditRequestModel(
                id_login=id_login,
                request=request_content,
                timestamp=timestamp_init,
                url=url,
            )
            audit_request = await AuditRequestDao().insert(dto)

            if audit_request:
                return audit_request.id

        except Exception as e:
            print("ERROR: Audit -> audit_request: " + str(e))

    async def _audit_response(id_request, response_result, timestamp_end):
        try:
            dto = AuditResponseModel(
                response=response_result,
                timestamp=timestamp_end,
                id_request=id_request,
            )

            return await AuditResponseDao().insert(dto)
        except Exception as e:
            print("ERROR: Audit -> audit_response: " + str(e))
