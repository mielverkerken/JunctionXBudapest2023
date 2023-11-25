from typing import Dict, List
import uuid

from .websocket_manager import WebSocketManager

from .secret import Secret

class SecretService:
    def __init__(self, websocket_manager: WebSocketManager):
        self.data : Dict[uuid.UUID, Secret] = {}
        self.websocket_manager = websocket_manager

    def save(self, secret: Secret) -> Secret:
        secret.id = str(uuid.uuid4())
        self.data[secret.id] = secret
        self.websocket_manager.update_secret(secret)
        return secret

    def save_all(self, secrets: List[Secret]) -> List[Secret]:
        return [self.save(secret) for secret in secrets]

    def read(self, id: uuid.UUID) -> Secret:
        if id not in self.data:
            raise Exception("No secret found with this ID.")
        return self.data[id]
    
    def read_all(self) -> List[Secret]:
        return list(self.data.values())

    def update(self, id: uuid.UUID, secret: Secret) -> None:
        if id not in self.data:
            raise Exception("No secret found with this ID.")
        self.data[id] = secret

    def delete(self, id: uuid.UUID) -> None:
        if id not in self.data:
            raise Exception("No secret found with this ID.")
        del self.data[id]