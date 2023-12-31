from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict
import uuid
import json

from nightfall import Finding
from .source import Source

CONTEXT_BYTES = 20

@dataclass
class Detector():
    """Detector describes the type of detector that found the secret."""
    name : str
    provider : str
    properties : Dict[str, str] = None

    def to_dict(self):
        return asdict(self)

class Confidence(Enum):
    """Confidence describes the certainty that a piece of content matches a detector."""
    VERY_UNLIKELY = "VERY_UNLIKELY"
    UNLIKELY = "UNLIKELY"
    POSSIBLE = "POSSIBLE"
    LIKELY = "LIKELY"
    VERY_LIKELY = "VERY_LIKELY"

    def to_dict(self):
        return self.value

@dataclass
class Range():
    """Range describes the location of a secret in a piece of content."""
    start: int
    end: int

    def to_dict(self):
        return asdict(self)


@dataclass
class Secret:
    value: str
    detector: Detector
    confidence: Confidence
    secret_type: str
    context_before: str = None
    context_after: str = None
    range: Range = None
    id: uuid.UUID = str(uuid.uuid4())
    source_id: uuid.UUID = None

    @classmethod
    def create(cls, **kwargs):
        return cls(
            value=kwargs.get('value'),
            detector=Detector(**kwargs.get('detector')),
            confidence=Confidence(kwargs.get('confidence')),
            secret_type=kwargs.get('secret_type'),
            context_before=kwargs.get('context_before'),
            context_after=kwargs.get('context_after'),
            range=kwargs.get('range'),
            id=str(uuid.uuid4()),
            source_id=kwargs.get('source_id')
        )

    @classmethod
    def from_nightfall_finding(cls, finding: Finding, source: Source):
        context_before = finding.before_context 
        context_after = finding.after_context
        if context_before is None:
            start = max(0, finding.byte_range.start - CONTEXT_BYTES)
            end = finding.byte_range.start
            context_before = source.content[start:end]
        if context_after is None:
            start = finding.byte_range.end
            end = min(len(source.content), finding.byte_range.end + CONTEXT_BYTES)
            context_after = source.content[start:end]
        return cls(
            value=finding.finding,
            detector=Detector(finding.detector_name, "NightFallAPI"),
            context_before=context_before,
            context_after=context_after,
            range=Range(finding.byte_range.start, finding.byte_range.end),
            secret_type=finding.detector_name,
            confidence=Confidence(finding.confidence.name),
            source_id=source.id,
        )
    
    @classmethod
    def from_regex_match(cls, match: dict, source: Source):
        context_before = source.content[max(0, match['byte_start'] - CONTEXT_BYTES):match['byte_start']]
        context_after = source.content[match['byte_end']:min(len(source.content), match['byte_end'] + CONTEXT_BYTES)]
        return cls(
            value=match['value'],
            detector=Detector(match['pattern_name'], "RegexDetector", {"regex_pattern": match['regex_pattern']}),
            context_before=context_before,
            context_after=context_after,
            range=Range(match['byte_start'], match['byte_end']),
            secret_type=match['secret_type'],
            confidence=Confidence.VERY_LIKELY if match['confidence'] == 'high' else Confidence.UNLIKELY,
            source_id=source.id,
        )
    
    def to_dict(self):
        return {
            "value": self.value,
            "detector": self.detector.to_dict(),
            "confidence": self.confidence.to_dict(),
            "secret_type": self.secret_type,
            "context_before": self.context_before,
            "context_after": self.context_after,
            "range": self.range.to_dict() if self.range else None,
            "id": str(self.id),
            "source_id": str(self.source_id) if self.source_id else None
        }

    def to_json(self):
        return json.dumps(self.to_dict())
