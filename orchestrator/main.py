from typing import Dict, List
from fastapi import FastAPI, BackgroundTasks
from orchestrator.secret import Secret
from orchestrator.secret_service import SecretService
from pydantic import BaseModel
import json
import os
from orchestrator.detectors.detector import DetectorService
from orchestrator.detectors.nightfallAPIConnector import NightFallAPIConnector


app = FastAPI()
secret_service = SecretService()
detector_service = DetectorService(secret_service)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/secrets")
async def get_secrets():
    return secret_service.data

@app.post("/secrets/scan-text")
async def secret_text(background_tasks: BackgroundTasks, body: Dict):
    background_tasks.add_task(detector_service.scan_text_for_secrets, body.get("data"))
    return {"message": "Scan successfully started."}


# CRUD endpoints for secrets
@app.post("/secret/")
async def create_secret(secret: Secret):
    secret_service.save(secret)
    return {"data": secret}

@app.get("/secret/{id}")
async def read_secret(id: str):
    secret = secret_service.read(id)
    return {"data": secret}

@app.put("/secret/{id}")
async def update_secret(id: str, secret: Secret):
    secret_service.update(id, secret)
    return {"data": secret}

@app.delete("/secret/{id}")
async def delete_secret(id: str):
    secret_service.delete(id)
    return 
