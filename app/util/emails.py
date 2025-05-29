import os
from email.message import EmailMessage

import aiosmtplib
from dotenv import load_dotenv

load_dotenv()


async def send_email_async(subject: str, to_email: str, body: str):
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
