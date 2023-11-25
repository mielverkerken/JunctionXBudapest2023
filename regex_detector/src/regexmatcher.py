from typing import List
from .pattern import Pattern
import yaml
import re


class RegexMatcher:
    patterns: List[Pattern] = None

    def __init__(self, file_path: str):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            self.patterns = [Pattern(**pattern['pattern']) for pattern in data['patterns']]

    def bulk_pattern_matcher(self, content: str):
        results = [
            {
                'value': match.group(),
                'pattern_name': pattern.name,
                'confidence': pattern.confidence,
                'secret_type': pattern.secret_type,
                'regex_pattern': pattern.regex,
                'byte_start': match.start(),
                'byte_end': match.end()
            }
            for pattern in self.patterns
            for match in re.finditer(pattern.compiled_regex, content)
        ]
        return results