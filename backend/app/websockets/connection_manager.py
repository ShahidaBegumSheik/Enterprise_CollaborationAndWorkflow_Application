from fastapi import WebSocket
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
            
    async def send_to_user(self, user_id: int, message: dict):
        connections = self.active_connections.get(user_id, [])

        for websocket in connections:
            await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for connections in self.active_connections.values():
            for websocket in connections:
                await websocket.send_json(message)

manager = ConnectionManager()