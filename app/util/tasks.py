from config.celery_worker import celery_app
from util.emails import send_email


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_registration_email(self, email: str, username: str):
    subject = "Welcome to Our App!"
    body = f"Hi {username}, thank you for registering."
    send_email(subject, email, body)
