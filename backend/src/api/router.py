from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from src.logging.logger import Logger, ErrorLogger
from src.core.ScanManager import ScanManager


class TextQuery(BaseModel):
    query: str

router = APIRouter()

@router.get("/health")
def get_health():
    Logger().info("Checked for server health, status : ok")
    return {"status" : "ok"}

@router.post("/api/query/text")
def handle_text_query(request: TextQuery):
    Logger().info("Got the query through /api/query/text")
    return {
        "received" : request.query
    }

@router.post("/api/query/voice")
async def handle_voice_query(audio: UploadFile = File(...)):
    print(audio.filename)
    print(audio.content_type)
    return {
        "filename" : audio.filename,
        "content_type" : audio.content_type
    }

@router.post("/api/source")
def handle_source(request: TextQuery):
    print("source" + request.query)
    scan_manager = ScanManager(TextQuery.query)
    # scan_manager.scan()
    return {
        "source_received" : request.query
    }