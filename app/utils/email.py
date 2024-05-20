from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
import jwt
from core.security import settings
from db.models.user import User

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

# logger
import logging

logger = logging.getLogger("email_verification")


conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL,
    MAIL_PASSWORD=settings.EMAIL_PWD,
    MAIL_FROM=settings.EMAIL,
    MAIL_PORT= 465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


@post_save(User)
async def send_verfication_email(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str]
) -> None:
      
      if created:
        try:
            await send_email([instance.email], instance)
        except Exception as e:
            logger.error(f"Error sending email: {e}")


async def send_email(email: List, instance: User):
    try:
        background_tasks = BackgroundTasks()
        token_data = {
            "id": instance.id,
            "username": instance.username
        }

        token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITM)

        template = f"""
            <!DOCTYPE html>
            <html>
                <head>
                </head>
                <body>
                    <div style = "display: flex; align-items: center; justify-comtent: center; flex-direction: column">

                        <h3>Account Verification</h3>
                        <br>

                        <p>Thanks for choosing BioGrowth, please click on the button below to verify your account</p>

                        <a style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem;
                        font-size: 1rem; text-decoration: none; background: #0275d8; color: white"
                        href="http://localhost:8000/auth/verification/?token={token}">
                        Verify my email
                        </a>

                        <p>Please kindly ignore this email if you did not register for BioGrowth. Thanks</p>

                    </div>
                </body>
            </html>
        """

        message = MessageSchema(
            subject="BioGrowth Account Verification Email",
            recipients=email,
            body=template,
            subtype="html"
        )

        
        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        logger.info("Email sent successfully")

    except Exception as e:
        logger.error(f"Error in send_email function: {e}")