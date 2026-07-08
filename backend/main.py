from fastapi import FastAPI
from backend.db.database import engine, Base
from pydantic import BaseModel
#from backend.nlp.intent_extractor import extract_intent_slots
from backend.nlp.intent_adapter import adapt_intent_result
from backend.nlp.prompts import build_prompt
from backend.nlp.gemini_client import ask_gemini

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
            "intent": "book_op",
            "slots": {
                "doctor_name": None,
                "department": "Cardiology",
                "preferred_date": "Tomorrow",
                "preferred_time": None,
                "ticket_number": None
            }
       }
      intent_result=adapt_intent_result(user_text,extracted_result)

Base.metadata.create_all(bind=engine)

