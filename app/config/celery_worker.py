from celery import Celery
import asyncio
from util.emails import send_email_async

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_registration_email(self, email: str, username: str):
    subject = "Welcome to Our App!"
    body = f"Hi {username}, thank you for registering."
    asyncio.run(send_email_async(subject, email, body))