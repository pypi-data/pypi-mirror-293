from app.external_api.connection.connection import Connection
import os
from firebase_admin import credentials, initialize_app, get_app, _apps
from app.util import path as Path

# Ejemplo de uso:
#
#


class Firebase(Connection):
    # Url o dominio de la API

    def __init__(self):
        try:
            self.project_id = os.getenv("FIREBASE_PROJECT_ID")
            self.url = f"https://fcm.googleapis.com/v1/projects/{self.project_id}/messages:send"

            this_path = Path.get_current_path()
            self.cred = credentials.Certificate(f"{this_path}/service-account.json")

            if not _apps:
                initialize_app(self.cred)
            else:
                self.app = get_app()

        except Exception as e:
            print("ERROR: External Api Firebase -> init: " + str(e))

    async def _get_access_token(self):
        try:
            auth_token = self.cred.get_access_token()
            return auth_token.access_token

        except Exception as e:
            print("ERROR: External Api Firebase -> get_access_token: " + str(e))

        return None

    async def notification_push(
        self, content: dict, token: str = None, topic: str = None, data=None
    ):
        try:
            self.token_jwt = await self._get_access_token()

            # print(self.token_jwt)
            self.headers.update({"Content-Type": "application/json; UTF-8"})

            message = {"notification": content}

            if topic:
                message.update({"topic": topic})

            if token:
                message.update({"token": token})

            if data:
                message.update({"data": data})

            payload = {"message": message}

            # print(payload)

            response, _ = await self.post(json=payload)

            # print(response)
            # print(response.json())

            return response.status_code == 200

        except Exception as e:
            print("ERROR: External Api Firebase -> notifications_push: " + str(e))

        return False
