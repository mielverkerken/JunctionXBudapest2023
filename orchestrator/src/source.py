import uuid
from dataclasses import dataclass


@dataclass
class Source:
    """Source describes a submitted document for scanning."""
    content: str
    type: str = "API"
    id: uuid.UUID = str(uuid.uuid4())