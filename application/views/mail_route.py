from application.controllers.email import IMail, Email
from application.models.core import app, Depends
from application.models.libs.jwt import AuthJWT, validate_token

@app.post('/contact', tags = ['Mailing'])
def send_contact_email(emaildata: IMail, Authorize: AuthJWT = Depends(), operation_id="authorize"):
    validate_token(Authorize)
    return Email.contact(emaildata)

