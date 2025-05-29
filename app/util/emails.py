import os
from email.message import EmailMessage

import aiosmtplib
from dotenv import load_dotenv

load_dotenv()


async def send_email_async(subject: str, to_email: str, body: str):
    """
    The function `send_email_async` sends an email asynchronously using SMTP with the specified subject,
    recipient, and body.

    :param subject: The `subject` parameter is a string that represents the subject of the email you
    want to send. It typically describes the purpose or topic of the email content
    :type subject: str
    :param to_email: The `to_email` parameter is the email address of the recipient to whom you want to
    send the email. It is the email address where the email message will be delivered
    :type to_email: str
    :param body: The `body` parameter in the `send_email_async` function represents the content or
    message body of the email that you want to send. This is where you would include the actual text of
    the email message that you want the recipient to see when they open the email
    :type body: str
    """
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.getenv("EMAIL_SENDER_ADDRESS")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = to_email
    msg.set_content(body)

    await aiosmtplib.send(
        msg,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        start_tls=True,
    )
