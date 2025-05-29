import asyncio

from celery import Celery
from util.emails import send_email_async

# The line `celery_app = Celery("worker", broker="redis://localhost:6379/0",
# backend="redis://localhost:6379/0")` in the Python code snippet is creating an instance of a Celery
# application named "worker" with specific configurations for the message broker and result backend.
celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# The `celery_app.conf.update()` method is used to update the configuration settings of the Celery
# application (`celery_app`). In this specific case:
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

"""
    The function `send_registration_email` is a Celery task that sends a registration email to a user
    asynchronously using asyncio.

    :param email: The `email` parameter in the `send_registration_email` function is a string that
    represents the email address of the user to whom the registration email will be sent
    :type email: str
    :param username: The `username` parameter in the `send_registration_email` function is a string
    variable that represents the username of the user who is registering for the app. It is used to
    personalize the registration email message by addressing the user with their username
    :type username: str
    """


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_registration_email(self, email: str, username: str):
    subject = "Welcome to Our App!"
    body = f"Hi {username}, thank you for registering."
    asyncio.run(send_email_async(subject, email, body))
