from typing import Dict, List
import uuid

from orchestrator.secret import Secret

class SecretService:
    def __init__(self):
        self.data : Dict[uuid.UUID, Secret] = {}

    def save(self, secret: Secret) -> None:
        id = str(uuid.uuid4())
        self.data[id] = secret

    def save_all(self, secrets: List[Secret]) -> None:
        for secret in secrets:
            self.save(secret)

    def read(self, id: uuid.UUID) -> Secret:
        if id not in self.data:
            raise Exception("No secret found with this ID.")
        return self.data[id]

    def update(self, id: uuid.UUID, secret: Secret) -> None:
        if id not in self.data:
            raise Exception("No secret found with this ID.")
        self.data[id] = secret

    def delete(self, id: uuid.UUID) -> None:
        if id not in self.data:
            raise Exception("No secret found with this ID.")
        del self.data[id]