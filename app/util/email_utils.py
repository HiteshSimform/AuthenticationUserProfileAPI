import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def get_env_var(name: str) -> str:
    """
    The function `get_env_var` retrieves the value of a specified environment variable and raises an
    error if the variable is not set.

    :param name: The `name` parameter in the `get_env_var` function is a string that represents the name
    of the environment variable that you want to retrieve the value for
    :type name: str
    :return: The function `get_env_var` is returning the value of the environment variable with the name
    specified in the `name` parameter. If the environment variable is not set, it will raise a
    `ValueError` with a message indicating that the environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set")
    return value


SMTP_SERVER = get_env_var("SMTP_SERVER")
SMTP_PORT = int(get_env_var("SMTP_PORT"))
EMAIL_ADDRESS = get_env_var("EMAIL_SENDER_ADDRESS")
EMAIL_PASSWORD = get_env_var("EMAIL_SENDER_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    """
    The function `send_email` sends an email with a specified subject and body to a given email address.

    :param to_email: The `to_email` parameter is the email address of the recipient to whom you want to
    send the email. It should be a string containing the email address where you want the email to be
    delivered
    :type to_email: str
    :param subject: The `subject` parameter in the `send_email` function is a string that represents the
    subject of the email you want to send. It is the title or brief description of the content of the
    email
    :type subject: str
    :param body: The `body` parameter in the `send_email` function refers to the content or message that
    you want to include in the email being sent. This is where you would typically write the main text
    of the email, including any information, instructions, or details you want to communicate to the
    recipient
    :type body: str
    """
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
