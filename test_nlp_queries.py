# test_nlp_queries.py — run from project root: python test_nlp_queries.py

from backend.nlp.intent_extractor import extract_intent_slots, load_model
from backend.nlp.intent_adapter import adapt_intent_result

print("Loading model...")
if not load_model():
    print("Model failed to load. Check models/intent_classifier/ exists.")
    exit(1)

test_queries = [
    # Group 1 — plain English phrasing (the bug we found)
    "Cardiology doctors tomorrow",
    "Doctors available in Cardiology tomorrow",
    "Show me Cardiology doctors",
    "Is there a Cardiology doctor available",
    "List doctors in Neurology today",

    # Group 2 — plain English, other departments
    "ENT doctors today",
    "Orthopaedics doctor available tomorrow",
    "Any doctors in Dermatology",

    # Group 3 — minimal extra words
    "Cardiology",
    "Cardiology today",
    "Cardiology tomorrow",

    # Group 4 — doctor_availability without department
    "Is any doctor available today",
    "Doctor available now",

    # Group 5 — token_booking, plain English
    "Book a token for Cardiology",
    "I want to book an appointment tomorrow",
    "Book me a slot with a Cardiology doctor",

    # Group 6 — op_enquiry
    "What are your OP timings",
    "Is the hospital open today",
    "What departments do you have",

    # Group 7 — token_status
    "What is the status of my token",
    "Check my token number",
    "Has my token been called",

    # Group 8 — symptom-based
    "I have chest pain",
    "My knee hurts, is a doctor available",
]

for query in test_queries:
    extracted = extract_intent_slots(query)
    adapted = adapt_intent_result(query, extracted)

    print(f"\nQuery: {query}")
    print(f"  Intent: {extracted.get('intent')} (confidence: {extracted.get('confidence')})")
    print(f"  Slots:  {extracted.get('slots')}")