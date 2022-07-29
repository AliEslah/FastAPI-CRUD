import os

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()


class Envs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
    MAIL_TLS = os.getenv("MAIL_TLS")


MAIL_SSL = False
USE_CREDENTIALS = True
TEMPLATE_FOLDER = "api/templates"

config = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_TLS=Envs.MAIL_TLS,
    MAIL_SSL=MAIL_SSL,
    USE_CREDENTIALS=USE_CREDENTIALS,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER,
)


async def send_registration_mail(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject, recipients=[email_to], template_body=body, subtype="html"
    )

    fm = FastMail(config)

    await fm.send_message(message=message, template_name="email.html")
