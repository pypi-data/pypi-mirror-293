import os
from jinja2 import Environment, FileSystemLoader

from app.module.smtp.localhost import Localhost
from app.util import path as Path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from app.external_api.gmail.gmail import Gmail


class Smtp:

    def __init__(self):
        self.from_email = os.getenv("LOCALHOST_SMTP_EMAIL")

    def send_simple_email(self, email: str, subject: str, body: str):
        message = self._new_message(email, subject)

        message.attach(MIMEText(body, "plain"))

        return self._send(email, message)

    def send_template_email(
        self,
        email: str,
        subject: str,
        content: dict,
        template_name: str,
        images: list = [],
    ):
        try:
            html_content = self._render_template(template_name, content)

            if not html_content:
                return False

            message = self._new_message(email, subject)

            # Adjuntar el cuerpo del mensaje HTML.
            msg_alternative = MIMEMultipart("alternative")
            message.attach(msg_alternative)
            msg_text = MIMEText(html_content, "html")
            msg_alternative.attach(msg_text)

            # Adjuntar imágenes embebidas.
            for img_path in images:
                with open(img_path, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-ID", f"<{os.path.basename(img_path)}>")
                    message.attach(img)

            return self._send(email, message)

        except Exception as e:
            print("ERROR: Module Smtp -> send: " + str(e))

        return False

    def _new_message(self, email, subject) -> MIMEMultipart:
        try:
            message = MIMEMultipart("related")
            message["From"] = self.from_email
            message["To"] = email
            message["Subject"] = subject

            return message

        except Exception as e:
            print("ERROR: Module Smtp -> new_message: " + str(e))

        return None

    def _send(self, email, message: MIMEMultipart) -> bool:
        try:
            # return Gmail(None).send_email(email, message)
            return Localhost.send_email(email, message=message)

            # result, token = Gmail(None).send_email(message)

            # print(result, token)

            # return result

        except Exception as e:
            print("ERROR: Module Smtp -> send: An error occurred: " + str(e))

    def _render_template(self, template_name, content):
        try:
            root_path = Path.get_previous_path(previous=1)

            self.template_loader = FileSystemLoader(
                searchpath=f"{root_path}/resource/template/email"
            )

            self.template_env = Environment(loader=self.template_loader)

            template = self.template_env.get_template(template_name)

            return template.render(content)

        except Exception as e:
            print("ERROR: Module Smtp -> render_template: " + str(e))

        return None
