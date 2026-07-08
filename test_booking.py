from backend.nlp.gemini_client import ask_gemini
from backend.config import GEMINI_API_KEY
from backend.nlp.prompts import build_prompt
intent_result = {
    "intent": "book_op",
    "user_query": "I need a cardiologist tomorrow",
    "department": "Cardiology",
    "doctor": None,
    "date": "Tomorrow"
}

database_result = [
    {
        "doctor_name": "Dr. Ramesh",
        "department": "Cardiology",
        "time": "9 AM - 1 PM",
        "tokens_left": 12
    }
]
prompt=build_prompt(
    intent_result,
    database_result
)
print("========== GENERATED PROMPT ==========")
print(prompt)

print("\n========== GEMINI RESPONSE ==========")

reply = ask_gemini(prompt)

print(reply)