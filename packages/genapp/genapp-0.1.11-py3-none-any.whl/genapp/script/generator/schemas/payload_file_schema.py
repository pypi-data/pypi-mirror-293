from app.CRUD_KEY.DATABASE_NAME_KEY.API_AUDIT_PAYLOAD_KEY_dao import (
    API_AUDIT_PAYLOAD_CLASS_KEYDao,
)
from app.MODEL_KEY.DATABASE_NAME_KEY.API_AUDIT_PAYLOAD_KEY import (
    API_AUDIT_PAYLOAD_CLASS_KEYModel,
)


class Payload:
    async def audit(id_conn, payload):
        try:
            dto = API_AUDIT_PAYLOAD_CLASS_KEYModel(
                id_conn=id_conn, payload=payload)
            await API_AUDIT_PAYLOAD_CLASS_KEYDao().insert(dto)
        except Exception as e:
            print("ERROR: Audit Payload -> audit: " + str(e))
