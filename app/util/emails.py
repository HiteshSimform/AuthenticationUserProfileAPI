# from config.celery_worker import celery_app
# import aiosmtplib
# from email.message import EmailMessage
# from config.config import settings

# @celery_app.task(name="send_registration_email")
# def send_registration_email(to_email: str, username: str):
#     subject = "Welcome to Our App!"
#     content = f"Hello {username},\n\nThanks for registering with us."

#     message = EmailMessage()
#     message["From"] = settings.EMAIL_SENDER_ADDRESS
#     message["To"] = to_email
#     message["Subject"] = subject
#     message.set_content(content)

#     try:
#         aiosmtplib.send(
#             message,
#             hostname=settings.SMTP_SERVER,
#             port=settings.SMTP_PORT,
#             username=settings.EMAIL_SENDER_ADDRESS,
#             password=settings.EMAIL_SENDER_PASSWORD,
#             start_tls=True
#         )
#     except Exception as e:
#         print(f"Failed to send email: {e}")


import smtplib
from email.message import EmailMessage


def send_email(subject: str, to_email: str, body: str):
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "Chandreshkanzariya19123@gmail.com"
    EMAIL_HOST_PASSWORD = "jzdophxkuhbhucvh"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)
