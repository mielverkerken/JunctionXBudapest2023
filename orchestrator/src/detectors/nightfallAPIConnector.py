import os
from typing import List
from nightfall import Nightfall, Finding

from ..secret import Secret
from ..detectors.idetector import IDetector
from ..source import Source


class NightFallAPIConnector(IDetector):
    def __init__(self, api_key, detection_rule_uuid):
        self.api_key = api_key
        self.detection_rule_uuid = detection_rule_uuid
        self.nightfall = Nightfall()
    
    async def scan_text_for_secrets(self, sources: List[Source]) -> List[List[Secret]]:
        findings, _ = self.nightfall.scan_text(
            [source.content for source in sources],
            detection_rule_uuids=[os.environ['NIGHTFALL_DETECTION_RULE_UUID']],
        )
        secrets = [[Secret.from_nightfall_finding(finding, source) for finding in finding_for_text] for finding_for_text, source in zip(findings, sources)]
        return secrets
