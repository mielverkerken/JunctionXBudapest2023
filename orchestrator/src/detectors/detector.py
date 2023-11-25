from typing import List
import os

from ..source import Source
from ..secret_service import SecretService
from ..detectors.nightfallAPIConnector import NightFallAPIConnector
from .idetector import IDetector
from .regexdetector import RegexDetectorConnector
from ..secret import Secret
from fastapi import BackgroundTasks


class DetectorService:
    detectors: List[IDetector]

    def __init__(self, secret_service: SecretService):
        nightfall_detector = NightFallAPIConnector(os.environ['NIGHTFALL_API_KEY'], os.environ['NIGHTFALL_DETECTION_RULE_UUID'])
        regex_detector = RegexDetectorConnector(os.environ['REGEX_DETECTOR_URL'], os.environ['REGEX_DETECTOR_PORT'])
        self.detectors = [nightfall_detector, regex_detector]
        self.secret_service = secret_service

    async def scan_text_for_secrets(self, sources: List[Source], background_tasks: BackgroundTasks) -> List[Secret]:
        for detector in self.detectors:
            found_secrets = await detector.scan_text_for_secrets(sources)
            for found_secret in found_secrets:
                self.secret_service.save_all(found_secret, background_tasks)
        return