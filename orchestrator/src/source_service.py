from dataclasses import dataclass
from typing import Dict, List
import uuid

@dataclass
class Source:
    """Source describes a submitted document for scanning."""
    content: str
    id: uuid.UUID = str(uuid.uuid4())


class SourceService:
    def __init__(self):
        self.data : Dict[uuid.UUID, Source] = {}

    def save(self, source: Source) -> None:
        source.id = str(uuid.uuid4())
        self.data[source.id] = source
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