from typing import List, Dict
from fastapi import WebSocket

from .secret import Secret
from .source import Source

class WebSocketManager:
    def __init__(self):
        self.active_subscribers: Dict[str, List[WebSocket]] = {"SECRETS": [], "SOURCES": []}

    async def subscribe_on_topic(self, websocket: WebSocket, topic: str):
        if topic not in self.active_subscribers:
            await websocket.close(code=1000)
        else:
            await websocket.accept()
            self.active_subscribers[topic].append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_subscribers.remove(websocket)
        websocket.close(code=1000)

    async def update_secret(self, secret: Secret):
        for connection in self.active_subscribers['SECRETS']:
            await connection.send_text(secret)

    async def update_source(self, source: Source):
        for connection in self.active_subscribers['SOURCES']:
            await connection.send_text(source)