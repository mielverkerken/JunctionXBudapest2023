from typing import Dict, List
from fastapi import FastAPI, BackgroundTasks

from .source_service import SourceService, Source
from .secret import Secret
from .secret_service import SecretService
from pydantic import BaseModel
import json
import os
from .detectors.detector import DetectorService
from .detectors.nightfallAPIConnector import NightFallAPIConnector


app = FastAPI()
secret_service = SecretService()
source_service = SourceService()
detector_service = DetectorService(secret_service)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/secrets/scan-text")
async def secret_text(background_tasks: BackgroundTasks, body: Dict):
    sources = [Source(content=content) for content in body.get("data")]
    sources = source_service.save_all(sources)
    background_tasks.add_task(detector_service.scan_text_for_secrets, sources)
    return {"message": "Scan successfully started."}


# CRUD endpoints for secrets
@app.get("/secrets")
async def get_secrets():
    return secret_service.read_all()

@app.get("/secrets/{id}")
async def read_secret(id: str):
    secret = secret_service.read(id)
    return {"data": secret}

# CRUD endpoints for sources
@app.get("/sources")
async def get_sources():
    return source_service.read_all()

@app.get("/sources/{id}")
async def get_source(id: str):
    source = source_service.read(id)
    return {"data": source}
