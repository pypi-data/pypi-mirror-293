import smtplib
import os


class Outlook:

    def send_email(email, message):
        try:
            server = os.getenv("OUTLOOK_SMTP_SERVER")
            port = os.getenv("OUTLOOK_SMTP_PORT")
            username = os.getenv("OUTLOOK_SMTP_USERNAME")
            passwd = os.getenv("OUTLOOK_PASSWD")

            with smtplib.SMTP(server, port) as smtp:
                smtp.starttls()
                smtp.login(username, passwd)
                smtp.send_message(message)

            return True

        except Exception as e:
            print("ERROR: Module Smtp Outlook -> send_email: " + str(e))

        return False
