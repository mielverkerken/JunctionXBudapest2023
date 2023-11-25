from typing import List
from .idetector import IDetector
from ..secret import Secret
from ..source_service import Source
import requests


class RegexDetectorConnector(IDetector):
    def __init__(self, url: str, port: int) -> None:
        super().__init__()
        self.base_url = f"{url}:{port}"


    async def scan_text_for_secrets(self, sources: List[Source]) -> List[List[Secret]]:
        findings = []
        for source in sources:
            if source is not None and source.content is not None:
                response = requests.post(f"{self.base_url}/secrets/scan-text", json={"content": source.content})
                if response.status_code != 200:
                    raise Exception("Error while processing request by detection module")
                findings.append([Secret.from_regex_match(match, source) for match in response.json()["data"]])
        return findings
