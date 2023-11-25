from typing import Dict, Union, List
from pydantic import BaseModel
from fastapi import FastAPI
import uuid
import re
import json
from .regexmatcher import RegexMatcher


app = FastAPI()
regex_matcher = RegexMatcher("src/regex-db.yaml")

@app.get("/status")
def read_root():
    return {"status": "UP"}


@app.post('/secrets/scan-text')
async def scan_text(body: Dict):
    return {"data": regex_matcher.bulk_pattern_matcher(body.get("content"))}
    