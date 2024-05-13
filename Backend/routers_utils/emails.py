from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
import jwt
from models import User

from dotenv import dotenv_values

config_credentials = dotenv_values(".env")


conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["email"],
    MAIL_PASSWORD=config_credentials["password"],
    MAIL_FROM=config_credentials["email"],
    MAIL_PORT= 465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(email: List, instance: User):

    token_data = {
        "id": instance.id,
        "username": instance.username
    }

    token = jwt.encode(token_data, config_credentials["secret_key"], algorithm=config_credentials["algorithm"])

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
    await fm.send_message(message=message)