from application.controllers.demo import IRecord, ILogin, Demo, Session, Depends, get_db
from application.models.core import app
from application.models.libs.websocket import WebSocket, WebSocketDisconnect, manager, get_websocket_request
from application.models.libs.jwt import AuthJWT, validate_token

# sample websocket implementation of demo endpoint
@app.websocket("/demo/{client_id}")
async def websockets(websocket: WebSocket, client_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    await manager.connect(websocket, client_id)
    while True:
        try:
            response = await get_websocket_request(websocket)
            # print(Demo.getalldemodata(db))
            await manager.send_message(response['message'], websocket, response['uid'] or client_id)

        except WebSocketDisconnect as websocket_err:
            # print(websocket_err)
            await manager.send_message(f"Websocket closed with error", websocket, client_id)
            # await manager.broadcast(f"Websocket closed with error")
    manager.disconnect(websocket, client_id)

## sample rest api request
@app.get('/demo', tags = ['Demo'], operation_id="authorize")
def get_all_demo(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    return Demo.getalldemodata(db)

@app.post('/demo', tags = ['Demo'], operation_id="authorize")
def save_demo(demodata: IRecord, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    return Demo.savedemodata(db, demodata)

@app.post('/login', tags = ['Authentication'])
def auth_user(form_data: dict, Authorize: AuthJWT = Depends()):
    # form_data = dict(form_data)
    return Demo.savetoken(form_data, Authorize)

