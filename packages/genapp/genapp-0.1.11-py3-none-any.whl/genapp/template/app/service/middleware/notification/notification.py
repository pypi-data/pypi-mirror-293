from abc import ABC, abstractmethod

from app.service.middleware.audit.notification import Notification as AuditNotification
from app.util import string as St
import asyncio


class NotificationKeys:
    RECIPIENT_ID_USER = "id_user"
    RECIPIENT_USERNAME = "name"
    RECIPIENT_EMAIL = "email"
    RECIPIENT_FTOKEN = "ftoken"


# Define the abstract Notification class
class Notification(ABC):

    def __init__(self, id_notification):
        self.id_notification = id_notification

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_send = cls.send

        async def audited_send(self, user_recipient, content: dict, user=None):
            result = await original_send(self, user_recipient, content, user)

            if result:
                notification_type = St.text_to_snake(cls.__name__)

                id_user = None
                if user:
                    id_user = user.id

                asyncio.create_task(
                    AuditNotification.audit(
                        user_recipient.id,
                        id_user,
                        self.id_notification,
                        notification_type,
                        user_recipient.lang,
                    )
                )

            return result

        cls.send = audited_send

    @abstractmethod
    async def send(self, user, user_recipient, content: dict):
        pass

    @abstractmethod
    async def send_topic(self, user, topic: str, content: dict):
        pass

    @abstractmethod
    async def send_all(self, user, content: dict, topic: str):
        pass
