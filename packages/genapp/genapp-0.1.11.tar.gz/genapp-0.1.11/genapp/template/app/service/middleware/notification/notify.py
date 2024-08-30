from app.crud.genericapp.notification_event_dao import NotificationEventDao
from app.model.genericapp.notification_event import NotificationEventModel
from app.crud.genericapp.user_has_notification_dao import UserHasNotificationDao
from app.model.genericapp.user_has_notification import UserHasNotificationModel

from app.crud.genericapp.notification_content_dao import NotificationContentDao

from app.model.genericapp.notification import NotificationModel

from app.crud.schema.schema_genericapp import *
from app.model.genericapp.calendar_appointments import CalendarAppointmentsModel
from app.crud.genericapp.calendar_appointments_dao import CalendarAppointmentsDao

from app.service.middleware.notification.vector.notification_push import (
    NotificationPush,
)

from app.service.middleware.notification.vector.email import Email

from app.util import string as St
from fastapi.encoders import jsonable_encoder
import asyncio
import re


class NotifyKeys:
    TO_USER = "to_user"
    FUNCTION_HANDLER = "function_handler"
    ID_NOTIFICATION = "id_notification"
    TOPICS = "topics"
    CONTENT = "content"

    NOTIFICATION_PUSH = "notification_push"
    EMAIL = "email"

    # Keys para remplazar en el string de las notificaciones
    USER_RECIPIENT_KEY = "USER_RECIPIENT_KEY"
    USER_SENDER_KEY = "USER_SENDER_KEY"


class Notify:

    async def notify_by_email(id_notification, user_recipient, replace_list):
        model = NotificationModel(id=id_notification)
        content = await NotificationContentDao().get_content(model)

        if not isinstance(content, Exception):
            content_lang = Notify._get_content_lang(content, user_recipient.lang)

            content_final = Notify._replace_keys_content(
                content_lang, user_recipient=user_recipient, replace_list=replace_list
            )

            asyncio.create_task(
                Email(id_notification).send(user_recipient, content_final)
            )

    async def notify_event(id_funtionality, result_code, user, seed_notification):
        event = await Notify._get_notification_event(id_funtionality, result_code)

        if event is not None:
            to_user = event.get(NotifyKeys.TO_USER, None)
            topics = event.get(NotifyKeys.TOPICS, None)

            if topics:
                # Notificar por topic
                pass

            if to_user:
                function_handler = event.get(NotifyKeys.FUNCTION_HANDLER, None)
                id_notification = event.get(NotifyKeys.ID_NOTIFICATION, None)
                content = event.get(NotifyKeys.CONTENT, None)

                user_recipient = await Notify._get_user_recipient(
                    function_handler, seed_notification
                )

                settings = await Notify._get_notification_settings(
                    user_recipient, id_notification
                )

                # Titulo y body en el lenguaje del destinatario
                content_lang = Notify._get_content_lang(content, user_recipient.lang)

                content_final = Notify._replace_keys_content(
                    content_lang, user=user, user_recipient=user_recipient
                )

                asyncio.create_task(
                    Notify._send_notification_to_user(
                        id_notification,
                        user,
                        user_recipient,
                        content_final,
                        settings,
                    )
                )

    async def _send_notification_to_user(
        id_notification,
        user,
        user_recipient,
        content: dict,
        settings: dict,
    ):
        try:
            # Via NotificationPush
            if NotifyKeys.NOTIFICATION_PUSH in settings:
                if settings[NotifyKeys.NOTIFICATION_PUSH]:
                    asyncio.create_task(
                        NotificationPush(id_notification).send(
                            user_recipient, content, user=user
                        )
                    )

            # Via Email
            if NotifyKeys.EMAIL in settings:
                if settings[NotifyKeys.EMAIL]:
                    asyncio.create_task(
                        Email(id_notification).send(user_recipient, content, user=user)
                    )

        except Exception as e:
            print("ERROR: Notify -> send_notification_to_user:", str(e))

    def _get_content_lang(content, lang):
        if lang in content:
            return content[lang]

        return next(iter(content.values()))

    def _replace_keys_content(content, user=None, user_recipient=None, replace_list=[]):
        try:
            if user:
                replace_list.append(
                    (NotifyKeys.USER_SENDER_KEY, St.text_to_pascal(user.username))
                )

            if user_recipient:
                replace_list.append(
                    (
                        NotifyKeys.USER_RECIPIENT_KEY,
                        St.text_to_pascal(user_recipient.username),
                    )
                )

            content_replaced = {}
            # Iterar sobre las claves y valores en el diccionario content
            for key_dict, value in content.items():
                # Iterar sobre los elementos en replace_list
                for key_replace, new_content in replace_list:
                    # Crear un patrón de búsqueda para la clave específica
                    pattern = re.compile(re.escape(key_replace))
                    # Reemplazar la clave con el nuevo contenido en el valor actual
                    value = pattern.sub(new_content, value)
                content_replaced[key_dict] = value

            return content_replaced

        except Exception as e:
            print("ERROR: Notify -> replace_keys_content:", str(e))

        return None

    async def _get_user_recipient(function_handler: str, seed_notification) -> int:
        try:
            func = getattr(RecipientHandlerFunction, function_handler)
            if not func:
                print(
                    f"ERROR: Notify -> get_user_recipient: {function_handler} not implemented"
                )
                return None

            if seed_notification is not None:
                return await func(seed_notification)

        except Exception as e:
            print("ERROR: Notify -> get_user_recipient:", str(e))

        return None

    async def _get_notification_event(id_funtionality: int, result_code: str) -> dict:
        try:
            notification_model = NotificationEventModel(
                result_code=result_code, id_funtionality=id_funtionality
            )

            return await NotificationEventDao().get_notification_event(
                notification_model
            )

        except Exception as e:
            print("ERROR: Notify -> get_notification_event:", str(e))

        return None

    async def _get_notification_settings(user_recipient, id_notification: int) -> dict:
        try:
            if user_recipient:
                model = UserHasNotificationModel(
                    id_user=user_recipient.id, id_notification=id_notification
                )
                return await UserHasNotificationDao().get_types_notification(model)

        except Exception as e:
            print("ERROR: Notify -> get_notification_settings:", str(e))

        return None


class RecipientHandlerFunction:
    async def get_employee_from_appointment(
        appointment: CalendarAppointments,
    ) -> int:
        try:
            if isinstance(appointment, CalendarAppointments):
                return await CalendarAppointmentsDao().get_user_employee(appointment)

        except Exception as e:
            print(
                "ERROR: RecipientHandlerFunction -> get_employee_from_appointment:",
                str(e),
            )

        return None

    async def get_customer_from_appointment(
        appointment: CalendarAppointments,
    ) -> int:
        try:
            if isinstance(appointment, CalendarAppointments):
                return await CalendarAppointmentsDao().get_user_customer(appointment)

        except Exception as e:
            print(
                "ERROR: RecipientHandlerFunction -> get_customer_from_appointment:",
                str(e),
            )

        return None
