from abc import ABC, abstractmethod
from ..secret import Secret
from typing import List


class IDetector(ABC):
    @abstractmethod
    async def scan_text_for_secrets(self, text: List[str]) -> List[Secret]:
        pass