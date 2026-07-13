import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.nlp.intent_extractor import extract_intent_slots, load_model
from backend.nlp.intent_adapter import adapt_intent_result
from backend.nlp.prompts import build_prompt
from backend.nlp.gemini_client import ask_gemini
from backend.booking.op_schedule_lookup import (
    lookup_available_doctors, get_all_doctors, get_doctor_details, get_available_tokens
)
from backend.booking.token_booking import book_token, get_token_status
from backend.booking.hospital_lookup import lookup_hospital_info
from backend.booking.department_lookup import get_departments, get_department_by_name
from backend.audio_pipeline import process_audio
from backend.tts.speak import speak


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not load_model():
        raise RuntimeError("Failed to load NLP model")
    os.makedirs("audio/temp", exist_ok=True)
    yield

app = FastAPI(lifespan=lifespan)

os.makedirs("audio", exist_ok=True)
os.makedirs("audio/temp", exist_ok=True)
app.mount("/audio", StaticFiles(directory="audio"), name="audio")


class ChatRequest(BaseModel):
    message: str


class BookingRequest(BaseModel):
    schedule_id: int
    name: str
    phone: str | None = None
    age: int | None = None
    gender: str | None = None


class TTSRequest(BaseModel):
    text: str


def _empty_dept_fields():
    """Default department_id/department_name pair used when no department applies."""
    return {"department_id": None, "department_name": None}


def process_chat(user_text: str) -> dict:
    """
    Shared logic for /chat and /voice.
    Returns:
    {
        "text": str,
        "data": list|dict|None,
        "action": str|None,
        "department_id": int|None,
        "department_name": str|None
    }
    """
    extracted_result = extract_intent_slots(user_text)
    intent_result = adapt_intent_result(user_text, extracted_result)
    intent = intent_result.get("intent")
    print(f"DEBUG text reaching NLP: {repr(user_text)}")
    print(f"DEBUG intent_result: {intent_result}")
    if intent == "doctor_availability":
        department_name = intent_result.get("department")
        database_result = lookup_available_doctors(
            department=department_name,
            doctor=intent_result.get("doctor"),
            date=intent_result.get("date")
        )
        print(f"DEBUG — department extracted: {intent_result.get('department')}")
        if not database_result:
            return {
                "text": "No doctors found for your request.",
                "data": None,
                "action": None,
                **_empty_dept_fields()
            }

        prompt = build_prompt(intent_result, database_result)
        response = ask_gemini(prompt)
        text = response or "Sorry, the AI service is currently unavailable. Please try again later."

        dept_info = get_department_by_name(department_name) if department_name else None

        return {
            "text": text,
            "data": database_result,
            "action": "show_doctors",
            "department_id": dept_info["department_id"] if dept_info else None,
            "department_name": dept_info["department_name"] if dept_info else None
        }

    elif intent == "token_status":
        token_number = intent_result.get("ticket_number")
        if not token_number:
            return {
                "text": "Please provide your token number to check its status.",
                "data": None,
                "action": None,
                **_empty_dept_fields()
            }
        database_result = get_token_status(token_number)
        if not database_result or database_result.get("success") is False:
            return {
                "text": "Sorry, I couldn't find that token. Please check the number and try again.",
                "data": None,
                "action": None,
                **_empty_dept_fields()
            }
        prompt = build_prompt(intent_result, database_result)
        response = ask_gemini(prompt)
        text = response or "Sorry, the AI service is currently unavailable. Please try again later."
        return {
            "text": text,
            "data": database_result,
            "action": "show_token_status",
            **_empty_dept_fields()
        }

    elif intent == "op_enquiry":
        database_result = lookup_hospital_info()
        if not database_result:
            return {
                "text": "Sorry, hospital information is currently unavailable.",
                "data": None,
                "action": None,
                **_empty_dept_fields()
            }
        prompt = build_prompt(intent_result, database_result)
        response = ask_gemini(prompt)
        text = response or "Sorry, the AI service is currently unavailable. Please try again later."
        return {
            "text": text,
            "data": database_result,
            "action": None,
            **_empty_dept_fields()
        }

    elif intent == "token_booking":
        department_name = intent_result.get("department")

        if department_name:
            # Department already known from the user's message (e.g. "cardiology
            # doctor book cheyyanam") — skip straight to that department's doctors,
            # same as doctor_availability does.
            database_result = lookup_available_doctors(
                department=department_name,
                doctor=intent_result.get("doctor"),
                date=intent_result.get("date")
            )

            if not database_result:
                prompt = build_prompt(intent_result, None)
                response = ask_gemini(prompt)
                text = response or "Sorry, no doctors were found for that department right now."
                return {
                    "text": text,
                    "data": None,
                    "action": None,
                    **_empty_dept_fields()
                }

            prompt = build_prompt(intent_result, database_result)
            response = ask_gemini(prompt)
            text = response or "Sorry, the AI service is currently unavailable. Please try again later."

            dept_info = get_department_by_name(department_name)

            return {
                "text": text,
                "data": database_result,
                "action": "show_doctors",
                "department_id": dept_info["department_id"] if dept_info else None,
                "department_name": dept_info["department_name"] if dept_info else None
            }

        else:
            # No department mentioned yet — show the department list so the
            # user (or frontend) can pick one.
            departments = get_departments()
            prompt = build_prompt(intent_result, departments)
            response = ask_gemini(prompt)
            text = response or "Please select a department to proceed with booking."

            return {
                "text": text,
                "data": departments,
                "action": "show_departments",
                **_empty_dept_fields()
            }

    elif intent == "cancel_token":
        return {
            "text": "Token cancellation isn't available yet. Please contact the hospital reception directly if you need to cancel your appointment.",
            "data": None,
            "action": None,
            **_empty_dept_fields()
        }

    elif intent == "unclear":
        return {
            "text": "Sorry, could you please rephrase that?",
            "data": None,
            "action": None,
            **_empty_dept_fields()
        }

    else:
        return {
            "text": "Sorry, I couldn't understand your request.",
            "data": None,
            "action": None,
            **_empty_dept_fields()
        }


@app.get("/")
def home():
    return {"message": "Hospital OP Bot API Running"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        result = process_chat(request.message)
        return {
            "response": result["text"],
            "data": result["data"],
            "action": result["action"],
            "department_id": result["department_id"],
            "department_name": result["department_name"]
        }
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return {
            "response": "Sorry, something went wrong. Please try again.",
            "data": None,
            "action": None,
            "department_id": None,
            "department_name": None
        }


@app.post("/voice")
async def voice(audio: UploadFile = File(...)):
    try:
        input_path = "audio/temp/recording.wav"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        transcription_result = process_audio(input_path)
        if not transcription_result.get("success", False):
            error_message = (
                transcription_result.get("error")
                or transcription_result.get("message")
                or "Sorry, I couldn't understand the audio. Please try again."
            )
            return {
                "reply_text": error_message,
                "audio_url": None,
                "data": None,
                "action": None,
                "department_id": None,
                "department_name": None
            }

        user_text = transcription_result["transcript"]

        result = process_chat(user_text)

        tts_result = speak(result["text"])
        audio_url = None
        if tts_result.get("success", False):
            audio_url = f"/{tts_result['audio_path']}"

        return {
            "reply_text": result["text"],
            "audio_url": audio_url,
            "audio_base64": tts_result.get("audio_base64"),
            "data": result["data"],
            "action": result["action"],
            "department_id": result["department_id"],
            "department_name": result["department_name"]
        }
    except Exception as e:
        print(f"Voice endpoint error: {e}")
        return {
            "reply_text": "Sorry, something went wrong. Please try again.",
            "audio_url": None,
            "data": None,
            "action": None,
            "department_id": None,
            "department_name": None
        }


@app.post("/tts")
def tts(request: TTSRequest):
    result = speak(request.text)
    if not result.get("success", False):
        return {"success": False, "message": result.get("message", result.get("error", "TTS failed"))}
    return {
        "success": True,
        "audio_url": f"/{result['audio_path']}",
        "audio_base64": result.get("audio_base64")
    }


@app.get("/token_status")
def token_status(token_number: str):
    result = get_token_status(token_number)
    if not result or result.get("success") is False:
        return {"response": "Sorry, I couldn't find that token."}
    return result


@app.post("/book")
def book(request: BookingRequest):
    return book_token(
        schedule_id=request.schedule_id,
        name=request.name,
        phone=request.phone,
        age=request.age,
        gender=request.gender
    )


@app.get("/departments")
def departments():
    return get_departments()


@app.get("/doctors")
def doctors(department_id: int | None = None):
    result = get_all_doctors(department_id)
    if not result:
        return {"success": False, "message": "No doctors found."}
    return {"success": True, "doctors": result}


@app.get("/doctor/{doctor_id}")
def doctor_details(doctor_id: int):
    result = get_doctor_details(doctor_id)
    if not result:
        return {"success": False, "message": "Doctor not found."}
    return {"success": True, "doctor": result}


@app.get("/available-tokens/{doctor_id}")
def available_tokens(doctor_id: int):
    result = get_available_tokens(doctor_id)
    if not result:
        return {"success": False, "message": "No schedules found for this doctor."}
    return {"success": True, "available_tokens": result}