from typing import Dict, List
import uuid

from .websocket_manager import WebSocketManager

from .source import Source

class SourceService:
    def __init__(self, websocket_manager: WebSocketManager):
        self.data : Dict[uuid.UUID, Source] = {}
        self.websocket_manager = websocket_manager

    def save(self, source: Source) -> None:
        source.id = str(uuid.uuid4())
        self.data[source.id] = source
        self.websocket_manager.update_source(source)
        return source

    def save_all(self, sources: List[Source]) -> None:
        return [self.save(source) for source in sources]

    def read(self, id: uuid.UUID) -> Source:
        if id not in self.data:
            raise Exception("No source found with this ID.")
        return self.data[id]
    
    def read_all(self) -> List[Source]:
        return list(self.data.values())

    def update(self, id: uuid.UUID, source: Source) -> None:
        if id not in self.data:
            raise Exception("No source found with this ID.")
        self.data[id] = source

    def delete(self, id: uuid.UUID) -> None:
        if id not in self.data:
            raise Exception("No source found with this ID.")
        del self.data[id]