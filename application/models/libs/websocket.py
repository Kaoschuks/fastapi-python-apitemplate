from application.models.core import app, WebSocket, random, WebSocketDisconnect, Query

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict = {}

    async def connect(self, websocket: WebSocket, id: int):
        await websocket.accept()
        self.active_connections[id] = websocket

    async def disconnect(self, websocket: WebSocket, client_id: int):
        await websocket.send_text(f"client {client_id} disconnected")
        await websocket.close()
        del(self.active_connections[client_id])


    async def send_message(self, message: str, websocket: WebSocket, client_id: int):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json({
                'status': 200,
                'message': message
            })

    # async def broadcast(self, message: str):
    #     for i in self.active_connections:
    #         await self.active_connections[i].send_json({
    #             'status': 200,
    #             'message': message
    #         })

async def get_websocket_request(websocket: WebSocket):
    try:
        req = await websocket.receive_json()
        return dict(req) if req != None else {}
    except Exception as e:
        return { "error": e }

manager = ConnectionManager()