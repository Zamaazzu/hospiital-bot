from fastapi import FastAPI
from backend.db.database import engine, Base
from pydantic import BaseModel
#from backend.nlp.intent_extractor import extract_intent_slots
from backend.nlp.intent_adapter import adapt_intent_result
from backend.nlp.prompts import build_prompt
from backend.nlp.gemini_client import ask_gemini
from backend.booking.op_schedule_lookup import lookup_available_doctors
from backend.booking.token_booking import book_token, get_token_status
# Import all models
from backend.db.models import *

app = FastAPI()
class ChatRequest(BaseModel):          
        message:str
@app.get("/")
def home():
    return {"message": "Hospital OP Bot API Running"}


@app.post("/chat")
def chat(request:ChatRequest):
      user_text=request.message
      # Temporary mock until Person 3 integrates intent_extractor.py
      extracted_result = {
            "intent": "doctor_availability",
            "slots": {
                "doctor": None,
                "department": "Cardiology",
                "preferred_date": "2026-07-10",
                "preferred_time": None,
                "ticket_number": None
            }
        }
      intent_result=adapt_intent_result(user_text,extracted_result)
      intent=intent_result.get("intent")
      if intent == "doctor_availability":
            database_result = lookup_available_doctors(
            department=intent_result.get("department"),
            doctor=intent_result.get("doctor"),
            date=intent_result.get("date")
        )
            prompt=build_prompt(
                  intent_result,
                  database_result
            )
            response=ask_gemini(prompt)
            return{
                  "response":response
            }

      elif intent == "token_booking":
            pass

      elif intent == "token_status":
           pass
 
      elif intent == "op_enquiry":
           pass
      elif intent=="cancel_token":
            return{
                  "response":"Token cancellation not implemented yet"
            }
      else:
           return {
             "response": "Sorry, I couldn't understand your request."
        }

#Base.metadata.create_all(bind=engine)

