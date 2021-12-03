from src.models.core import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from typing import List

mail_secret = os.getenv("SECRET_KEY")

class EmailSchema(BaseModel):
    email: List[str] = []

class EmailLib(object):
    config: any = {}

    def __init__(self):
        try :
            self.config = ConnectionConfig(
                MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
                MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
                MAIL_FROM = os.getenv("MAIL_SENDER"),
                MAIL_PORT = os.getenv("MAIL_PORT"),
                MAIL_SERVER = os.getenv("MAIL_SERVER"),
                MAIL_TLS = True,
                MAIL_SSL = False,
                MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME"),
                USE_CREDENTIALS = bool(os.getenv("USE_CREDENTIALS")),
                VALIDATE_CERTS = os.getenv("VALIDATE_CERTS")
            )
        except Exception as e:
            raise Exception(str(e))

    async def send_email(self, subject, recipient_email, body: str, attach = None):
        try :
            message = MessageSchema(
                subject = subject,
                recipients = recipient_email,  # List of recipients, as many as you can pass 
                body = body,
                subtype = "html"
            )
            fm = FastMail(self.config)
            await fm.send_message(message)
        except Exception as e:
            raise Exception(str(e))

def generate_email_token(email, type = 'email-confirm'):
    return mail_secret.dumps(email, salt=type)

def confirm_email_token(token, type = 'email-confirm'):
    try :
        return mail_secret.loads(token, salt=type, max_age=3600)
    except SignatureExpired:
        return False
        