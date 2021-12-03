# from src.controllers.notification import *
from sqlalchemy.orm.session import Session
from src.models.configs.dbconfig import get_db
from src.models.core import app, Depends
from src.models.libs.jwt import AuthJWT, validate_token


@app.post('/message', tags = ['Messaging & Chats'], operation_id="authorize")
async def send_a_message(message_data: dict, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass

@app.delete('/message/<messageid>', tags = ['Messaging & Chats'], operation_id="authorize")
async def delete_message(messageid: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass

@app.post('/channels', tags = ['Messaging & Chats'], operation_id="authorize")
async def create_channel(channel_data: dict, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass


@app.get('/channels', tags = ['Messaging & Chats'], operation_id="authorize")
async def get_channel(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass

@app.get('/channels/<channelid>', tags = ['Messaging & Chats'], operation_id="authorize")
async def get_channel(channelid: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass


# @app.route('/channels/<channelid>', methods=['PUT'])

# def update_channel(channelid):
#     try:
#         return Channels.update_channel(channelid)
#     except Exception as e:
#         raise InvalidUsage(str(e), status_code=500)


# @app.route('/channels/<channelid>', methods=['DELETE'])
# def delete_channel(channelid):
#     try:
#         return Channels.delete_channel(channelid)
#     except Exception as e:
#         raise InvalidUsage(str(e), status_code=500)
