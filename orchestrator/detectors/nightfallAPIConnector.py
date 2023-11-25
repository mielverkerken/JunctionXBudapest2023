import os
from typing import List
from nightfall import Nightfall, Finding

from orchestrator.secret import Secret
from orchestrator.detectors.idetector import IDetector


class NightFallAPIConnector(IDetector):
    def __init__(self, api_key, detection_rule_uuid):
        self.api_key = api_key
        self.detection_rule_uuid = detection_rule_uuid
        self.nightfall = Nightfall()
    
    async def scan_text_for_secrets(self, text: List[str]) -> List[List[Secret]]:
        findings, _ = self.nightfall.scan_text(
            text,
            detection_rule_uuids=[os.environ['NIGHTFALL_DETECTION_RULE_UUID']],
        )
        print(findings)
        secrets = [[Secret.from_nightfall_finding(finding, content) for finding in finding_for_text] for finding_for_text, content in zip(findings, text)]
        return secrets
