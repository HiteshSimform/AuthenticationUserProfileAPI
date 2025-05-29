import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set")
    return value


SMTP_SERVER = get_env_var("SMTP_SERVER")
SMTP_PORT = int(get_env_var("SMTP_PORT"))
EMAIL_ADDRESS = get_env_var("EMAIL_SENDER_ADDRESS")
EMAIL_PASSWORD = get_env_var("EMAIL_SENDER_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    try:
        print("In try")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent")
    except Exception as e:
        print("Error : ", e)
