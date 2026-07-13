from backend.nlp.gemini_client import ask_gemini
from backend.nlp.prompts import build_prompt
#========general=========
print("=" * 60)
print("GENERAL PROMPT")
print("=" * 60)

intent_result = {
    "intent": "general",
    "user_query": "Hello"
}

print(build_prompt(intent_result))

#========booking==========


print("\n" + "=" * 60)
print("BOOKING PROMPT")
print("=" * 60)

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

print(build_prompt(intent_result, database_result))

#============doctor============
print("\n" + "=" * 60)
print("DOCTOR PROMPT")
print("=" * 60)

intent_result = {
    "intent": "doctor_availability",
    "user_query": "Which cardiologists are available tomorrow?",
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
    },
    {
        "doctor_name": "Dr. Priya",
        "department": "Cardiology",
        "time": "2 PM - 5 PM",
        "tokens_left": 8
    }
]

print(build_prompt(intent_result, database_result))


#============token=========
print("\n" + "=" * 60)
print("TOKEN PROMPT")
print("=" * 60)

intent_result = {
    "intent": "token_status",
    "user_query": "What is my token status?"
}

database_result = {
    "token_number": 25,
    "doctor_name": "Dr. Ramesh",
    "department": "Cardiology",
    "date": "Tomorrow",
    "status": "Waiting",
    "estimated_time": "10:45 AM"
}

print(build_prompt(intent_result, database_result))


print("\n" + "=" * 60)
print("HOSPITAL PROMPT")
print("=" * 60)

intent_result = {
    "intent": "hospital_info",
    "user_query": "What departments are available?"
}

database_result = {
    "hospital_name": "City Hospital",
    "address": "Kottayam",
    "contact": "9876543210",
    "departments": [
        "Cardiology",
        "Orthopaedics",
        "Neurology"
    ]
}

print(build_prompt(intent_result, database_result))