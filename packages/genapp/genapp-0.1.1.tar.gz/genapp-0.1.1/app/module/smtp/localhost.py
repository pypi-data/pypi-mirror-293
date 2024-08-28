import aiosmtplib
import os


class Localhost:

    async def send_email(email, message):
        try:
            server = os.getenv("LOCALHOST_SMTP_SERVER")
            port = os.getenv("LOCALHOST_SMTP_PORT")
            username = os.getenv("LOCALHOST_SMTP_USERNAME")
            passwd = os.getenv("LOCALHOST_SMTP_PASSWD")

            async with aiosmtplib.SMTP(hostname=server, port=port) as smtp:
                await smtp.starttls()
                await smtp.login(username, passwd)
                await smtp.send_message(message)

            return True

        except Exception as e:
            print("ERROR: Module Smtp Localhost -> send_email: " + str(e))

        return False
