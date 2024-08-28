from app.crud.genericapp.audit_payload_dao import (
    AuditPayloadDao,
)
from app.model.genericapp.audit_payload import (
    AuditPayloadModel,
)


class Payload:
    async def audit(id_conn, payload):
        try:
            dto = AuditPayloadModel(
                id_conn=id_conn, payload=payload)
            await AuditPayloadDao().insert(dto)
        except Exception as e:
            print("ERROR: Audit Payload -> audit: " + str(e))
