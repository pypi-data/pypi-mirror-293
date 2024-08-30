from app.external_api.connection.connection import Connection
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.util import path as Path
import google.auth.transport.requests
import base64


class Gmail(Connection):

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    credentials_file = "credentials.json"

    def __init__(self, token_jwt):
        self.token_jwt = token_jwt
        self.creds = None
        self._authenticate()

    def send_email(self, message):
        """Envía un correo electrónico a través de la API de Gmail."""
        try:
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

            raw_message = {"raw": raw}

            sent_message = (
                self.service.users()
                .messages()
                .send(userId="107542700090789336568", body=raw_message)
                .execute()
            )

            print("Message Id: %s" % sent_message["id"])

            return True, self.token_jwt

        except HttpError as e:
            print(e)
            pass

        except Exception as e:
            print(f"ERROR: Gmail -> send_email: An error occurred: " + str(e))

        return False, None

    def _authenticate(self):
        """Autentica con la API de Gmail y guarda las credenciales."""
        try:
            if self.token_jwt:
                self.creds = Credentials.from_authorized_user_info(
                    self.token_jwt, self.SCOPES
                )
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    this_path = Path.get_current_path()
                    cred_path = Path.get_path_file(this_path, self.credentials_file)

                    self.creds = service_account.Credentials.from_service_account_file(
                        cred_path, scopes=self.SCOPES
                    )

                    request = google.auth.transport.requests.Request()

                    self.creds.refresh(request)

                    print(self.creds)

                # Guardar el nuevo token JWT en self.token_jwt
                # self.token_jwt = {
                #     "token": self.creds.token,
                #     # "refresh_token": self.creds.refresh_token,
                #     "token_uri": self.creds.token_uri,
                #     "client_id": self.creds.client_id,
                #     "client_secret": self.creds.client_secret,
                #     "scopes": self.creds.scopes,
                # }

                print(self.creds.token)

            self.service = build("gmail", "v1", credentials=self.creds)

        except Exception as e:
            print("ERROR: Gmail -> authenticate: " + str(e))

    def _authenticatev2(self):
        """Autentica con la API de Gmail y guarda las credenciales."""
        try:
            if self.token_jwt:
                self.creds = service_account.Credentials.from_service_account_info(
                    self.token_jwt, self.SCOPES
                )
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    this_path = Path.get_current_path()
                    cred_path = Path.get_path_file(this_path, self.credentials_file)

                    print(cred_path)

                    self.creds = service_account.Credentials.from_service_account_file(
                        cred_path, scopes=self.SCOPES
                    )
                    self.creds = self.creds.with_subject("genericapp.noreply@gmail.com")
                    request = google.auth.transport.requests.Request()

                    self.creds.refresh(request)

                # # Guardar el nuevo token JWT en self.token_jwt
                self.token_jwt = {
                    "token": self.creds.token,
                    "refresh_token": self.creds.refresh_token,
                    "token_uri": self.creds.token_uri,
                    "client_id": self.creds.client_id,
                    "client_secret": self.creds.client_secret,
                    "scopes": self.creds.scopes,
                }

                print(self.creds)

            self.service = build("gmail", "v1", credentials=self.creds)
        except Exception as e:
            print("ERROR: Gmail -> authenticate: " + str(e))
