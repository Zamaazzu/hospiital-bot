# backend/nlp/test_muril.py

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.nlp.intent_extractor import extract_intent_slots, load_model

# Load model first
load_model()

# ── Standard Test Queries ─────────────────────────────────
test_queries = [
    # op_enquiry
    ("Cardiology OP undo?",                    "op_enquiry"),
    ("Is OP available in ENT today?",          "op_enquiry"),
    ("ഇന്ന് ഒ.പി ഉണ്ടോ?",                     "op_enquiry"),
    ("Neurology OP schedule?",                 "op_enquiry"),
    ("What time does OP start?",               "op_enquiry"),

    # doctor_availability
    ("Dr. John today available?",              "doctor_availability"),
    ("Dr. Reshma ഇന്ന് ഉണ്ടോ?",               "doctor_availability"),
    ("Is Dr. Priya on duty?",                  "doctor_availability"),
    ("Prof. Dr. Kasi free ano?",               "doctor_availability"),
    ("Dr. Anand nale undo?",                   "doctor_availability"),

    # token_booking
    ("Token book cheyyanam",                   "token_booking"),
    ("I need an appointment with Dr. Rahul",   "token_booking"),
    ("ഒ.പി ടോക്കൺ വേണം",                      "token_booking"),
    ("Book me a slot in Cardiology",           "token_booking"),
    ("Reserve a token for Dr. Priya",          "token_booking"),

    # token_status
    ("Ente token status entha?",               "token_status"),
    ("What is my token number?",               "token_status"),
    ("ടോക്കൺ കൺഫേം ആയോ?",                    "token_status"),
    ("How many people are ahead of me?",       "token_status"),
    ("Is my booking confirmed?",               "token_status"),

    # cancel_token
    ("Token cancel cheyyanam",                 "cancel_token"),
    ("varan budhimuttu ond",                  "cancel_token"),
    ("ടോക്കൺ ക്യാൻസൽ ചെയ്യണം",               "cancel_token"),
    ("Please cancel my token",                 "cancel_token"),
    ("Ente booking cancel cheyyu",             "cancel_token"),
]

# ── Real World Test Queries ───────────────────────────────
real_world_queries = [
    ("njan varaan patilla",          "cancel_token"),
    ("doctor undo?",                 "doctor_availability"),
    ("OP",                           "op_enquiry"),
    ("please help me book",          "token_booking"),
    ("token evide?",                 "token_status"),
    ("Monday ravile slot veno?",     "token_booking"),
    ("aaro doctore kanam",           "token_booking"),
    ("enthu cheyyum",                "op_enquiry"),
    ("cancel",                       "cancel_token"),
    ("book",                         "token_booking"),
    ("status",                       "token_status"),
    ("available?",                   "doctor_availability"),
    ("OP timing?",                   "op_enquiry"),
    ("token venda",                  "cancel_token"),
    ("appointment venam",            "token_booking"),
]

# ── Symptom-Based Test Queries ────────────────────────────
symptom_queries = [
    # Pure symptom complaints (should be token_booking)
    ("enikku nenju vedana undu",          "token_booking"),
    ("ente monu pani",                    "token_booking"),
    ("ente mol pani",                     "token_booking"),
    ("kalinu vedana undu",                "token_booking"),
    ("vayar vedana",                      "token_booking"),
    ("thalavedhana undu",                 "token_booking"),
    ("chevi vedana",                      "token_booking"),
    ("fever undu",                        "token_booking"),
    ("tol vedana",                        "token_booking"),
    ("cough undu",                        "token_booking"),

    # Symptom + doctor question (should be doctor_availability)
    ("nenju vedana undu, doctor undo?",  "doctor_availability"),
    ("ente monu pani, doctor available?", "doctor_availability"),
    ("fever undu, doctor free aano?",    "doctor_availability"),

    # Symptom + OP question (should be op_enquiry)
    ("vayar vedana undu, OP undo?",      "op_enquiry"),
    ("chevi vedana, OP timing enthu?",   "op_enquiry"),
    ("fever undu, OP open aano?",        "op_enquiry"),
]

# ── Run Standard Tests ────────────────────────────────────
print("=" * 60)
print("STANDARD TEST RESULTS")
print("=" * 60)

correct = 0
total   = len(test_queries)

for query, expected in test_queries:
    result = extract_intent_slots(query)
    intent = result["intent"]
    slots  = result["slots"]
    status = "✅" if intent == expected else "❌"

    if intent == expected:
        correct += 1

    print(f"\n{status} Query:    {query}")
    print(f"   Intent:   {intent} (expected: {expected})")
    print(f"   Slots:    {slots}")

print("\n" + "=" * 60)
print(f"Standard Accuracy: {correct}/{total} = {correct/total*100:.1f}%")
print("=" * 60)

# ── Run Real World Tests ──────────────────────────────────
print("\n" + "=" * 60)
print("REAL WORLD TEST RESULTS")
print("=" * 60)

rw_correct = 0
rw_total   = len(real_world_queries)

for query, expected in real_world_queries:
    result = extract_intent_slots(query)
    intent = result["intent"]
    slots  = result["slots"]
    status = "✅" if intent == expected else "❌"

    if intent == expected:
        rw_correct += 1

    print(f"\n{status} Query:    {query}")
    print(f"   Intent:   {intent} (expected: {expected})")
    print(f"   Slots:    {slots}")

print("\n" + "=" * 60)
print(f"Real World Accuracy: {rw_correct}/{rw_total} = {rw_correct/rw_total*100:.1f}%")
print("=" * 60)

# ── Run Symptom Tests ─────────────────────────────────────
print("\n" + "=" * 60)
print("SYMPTOM-BASED TEST RESULTS")
print("=" * 60)

symptom_correct = 0
symptom_total = len(symptom_queries)

for query, expected in symptom_queries:
    result = extract_intent_slots(query)
    intent = result["intent"]
    slots = result["slots"]
    has_symptom = slots.get("has_symptom", False)
    department = slots.get("department", "None")
    status = "✅" if intent == expected else "❌"

    if intent == expected:
        symptom_correct += 1

    print(f"\n{status} Query:    {query}")
    print(f"   Intent:   {intent} (expected: {expected})")
    print(f"   Dept:     {department}")
    print(f"   Symptom:  {has_symptom}")

print("\n" + "=" * 60)
print(f"Symptom Accuracy: {symptom_correct}/{symptom_total} = {symptom_correct/symptom_total*100:.1f}%")
print("=" * 60)

# ── Final Summary ─────────────────────────────────────────
print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"Standard Test:   {correct}/{total} = {correct/total*100:.1f}%")
print(f"Real World Test: {rw_correct}/{rw_total} = {rw_correct/rw_total*100:.1f}%")
print(f"Symptom Test:    {symptom_correct}/{symptom_total} = {symptom_correct/symptom_total*100:.1f}%")

overall_accuracy = (correct + rw_correct + symptom_correct) / (total + rw_total + symptom_total) * 100
print(f"Overall Accuracy: {overall_accuracy:.1f}%")

if overall_accuracy >= 85:
    print("\n✅ Model is performing excellently!")
elif overall_accuracy >= 75:
    print("\n⚠️  Model is performing well - acceptable for production")
else:
    print("\n❌ Model needs improvement")

print("=" * 60)

# ── Failed Queries Analysis ───────────────────────────────
print("\n--- FAILED QUERIES ANALYSIS ---")
all_queries = test_queries + real_world_queries + symptom_queries
for query, expected in all_queries:
    result = extract_intent_slots(query)
    intent = result["intent"]
    if intent != expected:
        print(f"❌ '{query}'")
        print(f"   Expected: {expected}")
        print(f"   Got:      {intent}")
        print(f"   Confidence: {result.get('confidence', 'N/A')}")
        print()