import os
from fastapi import FastAPI,UploadFile, File
from fastapi.responses import JSONResponse
import shutil

from pydantic.v1 import BaseModel
from tts.speak import speak
from audio_pipeline import process_audio
from db.database import engine, Base

# Import all models
from db.models import *

app = FastAPI()
Base.metadata.create_all(bind=engine)
class TTSRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Hospital OP Bot API Running"}
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    input_path = "audio/temp/recording.wav"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_audio(input_path)

    if not result.get("success", False):
        return JSONResponse(
            status_code=400,
            content=result
        )

    return JSONResponse(
        status_code=200,
        content=result
    )
@app.post("/tts")
def text_to_speech(request: TTSRequest):

    result = speak(request.text)

    if not result.get("success", False):
        return JSONResponse(
            status_code=400,
            content=result
        )

    return JSONResponse(
        status_code=200,
        content=result
    )
