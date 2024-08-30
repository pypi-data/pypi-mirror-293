from app.crud.genericapp.audit_notification_dao import (
    AuditNotificationDao,
)
from app.model.genericapp.audit_notification import (
    AuditNotificationModel,
)


class Notification:

    async def audit(id_user_recipient, id_user_sender, id_notification, type, lang):
        try:
            model = AuditNotificationModel(
                id_user_sender=id_user_sender,
                id_user_recipient=id_user_recipient,
                id_notification=id_notification,
                type=type,
                language=lang,
            )

            result = await AuditNotificationDao().insert(model)

        except Exception as e:
            print("ERROR: Audit Notification -> audit: " + str(e))
