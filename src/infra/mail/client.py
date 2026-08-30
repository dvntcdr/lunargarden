from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,  # type: ignore
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS
)


mail = FastMail(conf)


async def send_email(
    subject: str,
    recipients: list[str],
    body: str
) -> None:
    message = MessageSchema(
        subject=subject,
        body=body,
        recipients=recipients,  # type: ignore
        subtype=MessageType.html
    )
    await mail.send_message(message)
