from application.views.demo_route import *
from application.models.libs.jwt import AuthJWT, websocket_validate_token, Query
from application.models.core import custom_openapi, os
from application.models.libs.websocket import WebSocket, WebSocketDisconnect, manager, get_websocket_request


@app.on_event("startup")
async def startup_event():
    print("The api is been booted up")

#  sample rest api implememtation
@app.get('/')
def index(Authorize: AuthJWT = Depends(), operation_id="authorize"):
    validate_token(Authorize)
    return { 'documentation': "localhost:" + os.getenv("PORT") + "/redoc"}


@app.websocket('/ws')
# async def websockets(websocket: WebSocket, Authorize: AuthJWT = Depends(), token: str = Query(...)):
async def websockets(websocket: WebSocket):
    client_id = 1
    await manager.connect(websocket, client_id)
    # await websocket_validate_token(websocket, Authorize, token)
    while True:
        try:
            response = await get_websocket_request(websocket)
            await manager.send_message(response, websocket, response['uid'])
            # await manager.broadcast(f"Client says: {response}")

        except WebSocketDisconnect as websocket_err:
            print(websocket_err)
            await manager.send_message(f"Websocket closed with error", websocket, client_id)
            # await manager.broadcast(f"Websocket closed with error")
    manager.disconnect(websocket, client_id)

app.openapi = custom_openapi