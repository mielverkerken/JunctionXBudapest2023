from typing import List, Dict
from fastapi import WebSocket
import json

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

    def disconnect(self, websocket: WebSocket, topic: str):
        self.active_subscribers[topic].remove(websocket)
        websocket.close(code=1000)

    async def update_secret(self, secret: Secret):
        print("update secret wss")
        for connection in self.active_subscribers['SECRETS']:
            await connection.send_json(secret.to_dict())

    async def update_source(self, source: Source):
        print("update source wss")
        for connection in self.active_subscribers['SOURCES']:
            await connection.send_json(source.to_dict())