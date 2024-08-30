from app.external_api.firebase.firebase import Firebase
from app.crud.genericapp.firebase_token_dao import FirebaseTokenDao
from app.model.genericapp.firebase_token import FirebaseTokenModel
from app.service.middleware.notification.notification import Notification


class NotificationPushKeys:
    BODY = "np_body"
    TITLE = "np_title"


class NotificationPush(Notification):

    async def send(self, user_recipient, content: dict, user=None):
        try:
            model = FirebaseTokenModel(id_user=user_recipient.id)
            firebase_tokens = await FirebaseTokenDao().get_firebase_tokens(model)

            result = False

            message = {
                "title": content.get(NotificationPushKeys.TITLE, None),
                "body": content.get(NotificationPushKeys.BODY, None),
            }

            if firebase_tokens:

                for firebase_token in firebase_tokens:
                    token = firebase_token.token
                    if await Firebase().notification_push(message, token=token):
                        print("NotificationPush Succesfully")
                        result = True

            return result

        except Exception as e:
            print("ERROR: Notification NotificationPush -> send: " + str(e))

        return False

    async def send_topic():
        pass

    async def send_all():
        pass
