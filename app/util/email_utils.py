import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_ADDRESS = os.getenv("EMAIL_SENDER_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    try:
        print("In try")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            print(type(smtp))
            smtp.starttls()
            print("before")
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("After")
            smtp.send_message(msg)
        print("Email sent")
    except Exception as e:
        print("Error : ",e)
