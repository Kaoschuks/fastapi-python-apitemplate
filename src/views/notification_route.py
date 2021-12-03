from src.controllers.notification import *
from src.models.core import app, Depends

@app.post('/sendmail', tags = ['Notifications'])
async def send_contact_email(emaildata: IMail, operation_id="authorize"):
    return await Email.sendmail(emaildata)

@app.post('/sendbulkmail', tags = ['Notifications'])
async def send_contact_email(emaildata: IMail, operation_id="authorize"):
    return await Email.sendbulkmail(emaildata)


@app.post('/sendpush', tags = ['Notifications'])
def send_push(pushdata: dict, operation_id="authorize"):
    return PushNotify.send_fcm(pushdata)

