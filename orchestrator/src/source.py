import uuid
from dataclasses import dataclass
import json


@dataclass
class Source:
    """Source describes a submitted document for scanning."""
    content: str
    type: str = "API"
    id: uuid.UUID = str(uuid.uuid4())

    def to_dict(self):
        """Convert the dataclass instance to a dictionary."""
        return {"content": self.content, "type": self.type, "id": str(self.id)}

    def to_json(self):
        """Convert the dataclass instance to a JSON string."""
        return json.dumps(self.to_dict())