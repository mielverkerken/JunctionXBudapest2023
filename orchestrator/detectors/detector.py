from typing import List
import os
from orchestrator.secret_service import SecretService
from orchestrator.detectors.nightfallAPIConnector import NightFallAPIConnector
from .idetector import IDetector

from orchestrator.secret import Secret


class DetectorService:
    detectors: List[IDetector]

    def __init__(self, secret_service: SecretService):
        nightfall_detector = NightFallAPIConnector(os.environ['NIGHTFALL_API_KEY'], os.environ['NIGHTFALL_DETECTION_RULE_UUID'])
        self.detectors = [nightfall_detector]
        self.secret_service = secret_service

    async def scan_text_for_secrets(self, text: List[str]) -> List[Secret]:
        for detector in self.detectors:
            found_secrets = await detector.scan_text_for_secrets(text)
            for found_secret in found_secrets:
                self.secret_service.save_all(found_secret)
        return