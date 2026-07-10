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
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from backend.nlp.intent_extractor import extract_intent_slots, load_model
from backend.nlp.intent_adapter import adapt_intent_result
from backend.nlp.prompts import build_prompt
from backend.nlp.gemini_client import ask_gemini
from backend.booking.op_schedule_lookup import lookup_available_doctors,get_all_doctors,get_doctor_details,get_available_tokens
from backend.booking.token_booking import book_token, get_token_status
from backend.booking.hospital_lookup import lookup_hospital_info
from backend.booking.department_lookup import get_departments

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not load_model():
        raise RuntimeError("Failed to load NLP model")
    yield

app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str


class BookingRequest(BaseModel):
    schedule_id: int
    name: str
    phone: str | None = None
    age: int | None = None
    gender: str | None = None
@app.post("/book")
def book(request: BookingRequest):
    result = book_token(
        schedule_id=request.schedule_id,
        name=request.name,
        phone=request.phone,
        age=request.age,
        gender=request.gender
    )
    return result
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

@app.get("/departments")
def departments():
    return get_departments()


@app.get("/doctors")
def doctors(department_id: int | None = None):
    doctors = get_all_doctors(department_id)
    if not doctors:
        return {
            "success": False,
            "message": "No doctors found."
        }
    return {
        "success": True,
        "doctors": doctors
    }


@app.get("/doctor/{doctor_id}")
def doctor_details(doctor_id: int):
    result = get_doctor_details(doctor_id)

    if not result:
        return {
            "success": False,
            "message": "Doctor not found."
        }

    return {
        "success": True,
        "doctor": result
    }

@app.get("/available-tokens/{doctor_id}")
def available_tokens(doctor_id: int):
    result = get_available_tokens(doctor_id)

    if not result:
        return {
            "success": False,
            "message": "No schedules found for this doctor."
        }

    return {
        "success": True,
        "available_tokens": result
    }


@app.get("/token_status")
def token_status(token_number: str):
    result = get_token_status(token_number)
    if not result or result.get("success") is False:
        return {"response": "Sorry, I couldn't find that token."}
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        user_text = request.message
        extracted_result = extract_intent_slots(user_text)
        intent_result = adapt_intent_result(user_text, extracted_result)
        intent = intent_result.get("intent")

        if intent == "doctor_availability":
            database_result = lookup_available_doctors(
                department=intent_result.get("department"),
                doctor=intent_result.get("doctor"),
                date=intent_result.get("date")
            )
            if not database_result:
                return {"response": "No doctors found for your request."}

            prompt = build_prompt(intent_result, database_result)
            response = ask_gemini(prompt)

            if response is None:
                  return {
                        "response": "Sorry, the AI service is currently unavailable. Please try again later."
                  }

            return {"response": response}

        elif intent == "token_status":
            token_number = intent_result.get("ticket_number")
            if not token_number:
                return {"response": "Please provide your token number to check its status."}

            database_result = get_token_status(token_number)
            if not database_result or database_result.get("success") is False:
                return {"response": "Sorry, I couldn't find that token. Please check the number and try again."}

            prompt = build_prompt(intent_result, database_result)
            response = ask_gemini(prompt)

            if response is None:
                  return {
                        "response": "Sorry, the AI service is currently unavailable. Please try again later."
                  }

            return {"response": response}

        elif intent == "op_enquiry":
            database_result = lookup_hospital_info()
            if not database_result:
                return {"response": "Sorry, hospital information is currently unavailable."}

            prompt = build_prompt(intent_result, database_result)
            response = ask_gemini(prompt)

            if response is None:
                  return {
                        "response": "Sorry, the AI service is currently unavailable. Please try again later."
                  }

            return {"response": response}

        elif intent == "token_booking":
            return {"response": "Booking integration is under development."}

        elif intent == "cancel_token":
            return {"response": "Token cancellation not implemented yet"}

        elif intent == "unclear":
            return {"response": "Sorry, could you please rephrase that?"}

        else:
            return {"response": "Sorry, I couldn't understand your request."}

    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return {"response": "Sorry, something went wrong. Please try again."}
