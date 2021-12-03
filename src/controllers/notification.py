# from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from src.models.libs.mailing import EmailLib
from src.models.dbmodel.mail_model import IMail
from fastapi.responses import JSONResponse
from datetime import datetime
import ast

class PushNotify(object):
    def send_fcm():
        # curl()
        print("push notification")




class Email(object):
    async def sendmail(data: IMail):
        try:
            mailer = EmailLib()
            await mailer.send_email(
                data.subject, 
                [ data.email ], 
                data.message
            )
            return {
                "message": 'email sent'
            }
        except Exception as e:
            return JSONResponse( status_code = 500, content = { "error": str(e) })

    async def sendbulkmail(data: IMail):
        try:
            print(data.email)
            mailer = EmailLib()
            await mailer.send_email(
                data.subject, 
                data.email, 
                data.message
            )
            return {
                "message": 'email sent'
            }
        except Exception as e:
            return JSONResponse( status_code = 500, content = { "error": str(e) })
