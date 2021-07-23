# from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from application.models.libs.mailing import send_email
from application.models.dbmodel.mail_model import IMail
from datetime import datetime
import ast

class PushNotify(object):
    def send_fcm():
        # curl()
        print("push notification")

class Email(object):
    def contact(data: IMail):
        try:
            email = data.email
            subject = data.subject
            message = data.message
            send_email(subject, [email], message, True)
            return make_response({
                "message": 'email sent'
            }, 200)
        except Exception as e:
            raise Exception(str(e))
        
    # def send_email():
    #     try:
    #         email = request.json['email']
    #         sender = request.json['sender']
    #         subject = request.json['subject']
    #         message = request.json['message']
    #         send_email(subject, [email], message, True, '', sender)
    #         return make_response({
    #             "message": 'email sent'
    #         }, 200)
    #     except Exception as e:
    #         raise Exception(str(e))