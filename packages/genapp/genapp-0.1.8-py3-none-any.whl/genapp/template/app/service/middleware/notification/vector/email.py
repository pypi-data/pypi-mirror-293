from app.service.middleware.notification.notification import Notification
from app.module.smtp.smtp import Smtp


class EmailKeys:
    SUBJECT = "em_subject"
    BODY = "em_body"
    TEMPLATE = "em_template"


class Email(Notification):

    async def send(self, user_recipient, content: dict, user=None) -> bool:
        try:
            email_addr = user_recipient.email

            subject = content.get(EmailKeys.SUBJECT, None)
            template = content.get(EmailKeys.TEMPLATE, None)
            body = content.get(EmailKeys.BODY, None)

            if template:
                if await Smtp().send_template_email(
                    email_addr, subject, content, template
                ):
                    print("Notification Email Succesfully")
                    return True

            else:
                if await Smtp().send_simple_email(email_addr, subject, body):
                    print("Notification Email Succesfully")
                    return True

        except Exception as e:
            print("ERROR: Notification Email -> send: " + str(e))

        return False

    async def send_topic():
        pass

    async def send_all():
        pass
