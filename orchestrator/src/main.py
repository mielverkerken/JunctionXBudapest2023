from typing import Dict, List
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect

from .source import Source

from .source_service import SourceService
from .secret import Secret
from .secret_service import SecretService
from pydantic import BaseModel
import json
import os
from .detectors.detector import DetectorService
from .detectors.nightfallAPIConnector import NightFallAPIConnector
from .websocket_manager import WebSocketManager
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_manager = WebSocketManager()
secret_service = SecretService(websocket_manager)
source_service = SourceService(websocket_manager)
detector_service = DetectorService(secret_service)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/secrets/scan-text")
async def secret_text(background_tasks: BackgroundTasks, body: Dict):
    sources = [Source(content=content) for content in body.get("data")]
    sources = source_service.save_all(sources, background_tasks)
    background_tasks.add_task(detector_service.scan_text_for_secrets, sources, background_tasks)
    return {"message": "Scan successfully started."}


@app.post("/secrets/scan-email")
async def secret_text(background_tasks: BackgroundTasks, body: Dict):
    sources = [Source(content=content, type="M365 Mail") for content in body.get("data")]
    sources = source_service.save_all(sources, background_tasks)
    background_tasks.add_task(detector_service.scan_text_for_secrets, sources, background_tasks)
    return {"message": "Scan successfully started."}


# CRUD endpoints for secrets
@app.get("/secrets")
async def get_secrets():
    return secret_service.read_all()

@app.get("/secrets/{id}")
async def read_secret(id: str):
    secret = secret_service.read(id)
    return {"data": secret}

@app.post("/secrets")
async def create_secret(body: Dict, background_tasks: BackgroundTasks):
    source_type = body.get("source_type") if body.get("source_type") else "LSASS"
    source = Source(content=None, type=source_type)
    source = source_service.save(source, background_tasks)
    secret = Secret.create(**body.get("data"), source_id=source.id)
    secret = secret_service.save(secret, background_tasks)
    return {"data": secret}

# CRUD endpoints for sources
@app.get("/sources")
async def get_sources():
    return source_service.read_all()

@app.get("/sources/{id}")
async def get_source(id: str):
    source = source_service.read(id)
    return {"data": source}

## Websocket endpoint
@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    print("websocket connecting on " + topic)
    await websocket_manager.subscribe_on_topic(websocket, topic)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "disconnect":
                websocket_manager.disconnect(websocket, topic)
                break
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, topic)
    except Exception as e:
        print(e)
        websocket_manager.disconnect(websocket, topic)