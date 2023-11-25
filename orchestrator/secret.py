from enum import Enum
from dataclasses import dataclass

from nightfall import Finding

CONTEXT_BYTES = 20

@dataclass
class Detector():
    """Detector describes the type of detector that found the secret."""
    name : str
    provider : str

class Confidence(Enum):
    """Confidence describes the certainty that a piece of content matches a detector."""
    VERY_UNLIKELY = "VERY_UNLIKELY"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    VERY_LIKELY = "VERY_LIKELY"


@dataclass
class Secret:
    value: str
    detector: Detector
    context_before: str
    context_after: str
    confidence: Confidence

    @classmethod
    def from_nightfall_finding(cls, finding: Finding, content: str):
        context_before = finding.before_context 
        context_after = finding.after_context
        if context_before is None:
            start = max(0, finding.byte_range.start - CONTEXT_BYTES)
            end = finding.byte_range.start
            context_before = content[start:end]
        if context_after is None:
            start = finding.byte_range.end
            end = min(len(content), finding.byte_range.end + CONTEXT_BYTES)
            context_after = content[start:end]
        return cls(
            value=finding.finding,
            detector=Detector(finding.detector_name, "NightFallAPI"),
            context_before=context_before,
            context_after=context_after,
            confidence=Confidence(finding.confidence.name),
        )
