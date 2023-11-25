from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
import re


class Confidence(Enum):
    high = "high"
    low = "low"

class Pattern(BaseModel):
    name: str
    regex: str
    confidence: Confidence
    secret_type: str
    compiled_regex: Optional[Any] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.compiled_regex = re.compile(self.regex)