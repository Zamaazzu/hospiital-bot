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
    ("ടോക്കൺ കൺഫേം ആയോ?",          "token_status"),
    ("Ethra per ond ini",       "token_status"),
    ("Is my booking confirmed?",               "token_status"),

    # cancel_token
    ("Token cancel cheyyanam",                 "cancel_token"),
    ("varan budhimuttu ond",                   "cancel_token"),
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
    ("nenju vedana undu, doctor undo?",   "doctor_availability"),
    ("ente monu pani, doctor available?", "doctor_availability"),
    ("fever undu, doctor free aano?",     "doctor_availability"),
    ("vayar vedana undu, OP undo?",       "op_enquiry"),
    ("chevi vedana, OP timing enthu?",    "op_enquiry"),
    ("fever undu, OP open aano?",         "op_enquiry"),
]

# ── Doctor Availability Edge Cases ────────────────────────
edge_cases = [
    ("Cardiology doctors tomorrow",              "doctor_availability"),
    ("Doctors available in Cardiology tomorrow", "doctor_availability"),
    ("Show me Cardiology doctors",               "doctor_availability"),
    ("Is there a Cardiology doctor available",   "doctor_availability"),
    ("List doctors in Neurology today",          "doctor_availability"),
    ("ENT doctors today",                        "doctor_availability"),
    ("Any doctors in Dermatology",               "doctor_availability"),
    ("My knee hurts, is a doctor available",     "doctor_availability"),
    ("I have chest pain",                        "token_booking"),
    ("Book a token for Cardiology",              "token_booking"),
]


# ── Run Tests Function ────────────────────────────────────
def run_tests(test_set, test_name, show_dept=False):
    print(f"\n{'=' * 60}")
    print(f"{test_name} TEST RESULTS")
    print(f"{'=' * 60}")

    correct = 0
    total = len(test_set)

    for query, expected in test_set:
        result = extract_intent_slots(query)
        intent = result["intent"]
        slots = result["slots"]
        status = "✅" if intent == expected else "❌"

        if intent == expected:
            correct += 1

        print(f"\n{status} Query:    {query}")
        print(f"   Intent:   {intent} (expected: {expected})")
        if show_dept:
            print(f"   Dept:     {slots.get('department', 'None')}")
            print(f"   Symptom:  {slots.get('has_symptom', False)}")
        else:
            print(f"   Slots:    {slots}")

    print(f"\n{'=' * 60}")
    print(f"{test_name} Accuracy: {correct}/{total} = {correct/total*100:.1f}%")
    print(f"{'=' * 60}")

    return correct, total


# ── Execute All Tests ─────────────────────────────────────
standard_correct, standard_total     = run_tests(test_queries,      "STANDARD")
realworld_correct, realworld_total   = run_tests(real_world_queries, "REAL WORLD")
symptom_correct, symptom_total       = run_tests(symptom_queries,    "SYMPTOM-BASED", show_dept=True)
edge_correct, edge_total             = run_tests(edge_cases,         "DOCTOR AVAILABILITY EDGE CASES", show_dept=True)

# ── Final Summary ─────────────────────────────────────────
print(f"\n{'=' * 60}")
print("FINAL SUMMARY")
print(f"{'=' * 60}")
print(f"Standard Test:        {standard_correct}/{standard_total} = {standard_correct/standard_total*100:.1f}%")
print(f"Real World Test:      {realworld_correct}/{realworld_total} = {realworld_correct/realworld_total*100:.1f}%")
print(f"Symptom Test:         {symptom_correct}/{symptom_total} = {symptom_correct/symptom_total*100:.1f}%")
print(f"Edge Cases Test:      {edge_correct}/{edge_total} = {edge_correct/edge_total*100:.1f}%")

overall_correct = standard_correct + realworld_correct + symptom_correct + edge_correct
overall_total   = standard_total + realworld_total + symptom_total + edge_total
overall_accuracy = overall_correct / overall_total * 100

print(f"Overall Accuracy:     {overall_correct}/{overall_total} = {overall_accuracy:.1f}%")

if overall_accuracy >= 85:
    print("\n✅ Model is performing excellently!")
elif overall_accuracy >= 75:
    print("\n⚠️  Model is performing well - acceptable for production")
else:
    print("\n❌ Model needs improvement")

# ── Failed Queries Analysis ───────────────────────────────
print(f"\n{'=' * 60}")
print("FAILED QUERIES ANALYSIS")
print(f"{'=' * 60}")

all_tests = [
    (test_queries,      "Standard"),
    (real_world_queries,"Real World"),
    (symptom_queries,   "Symptom"),
    (edge_cases,        "Edge Case"),
]

any_failed = False
for test_set, test_name in all_tests:
    for query, expected in test_set:
        result = extract_intent_slots(query)
        intent = result["intent"]
        if intent != expected:
            any_failed = True
            print(f"❌ [{test_name}] '{query}'")
            print(f"   Expected:   {expected}")
            print(f"   Got:        {intent}")
            print(f"   Confidence: {result.get('confidence', 'N/A')}")
            print(f"   Slots:      {result.get('slots', {})}")
            print()

if not any_failed:
    print("🎉 No failed queries! Perfect performance!")

print(f"{'=' * 60}")

# Debug department extraction
print("\n" + "=" * 60)
print("DEBUG: Department Extraction")
print("=" * 60)

from backend.nlp.intent_extractor import extract_department

test_depts = [
    "Cardiology doctors tomorrow",
    "Show me Cardiology doctors",
    "Is OP available in ENT today",
    "Doctors available in Cardiology tomorrow",
    "Any doctors in Dermatology",
]

for query in test_depts:
    dept = extract_department(query)
    print(f"'{query}' → {dept}")

# Comprehensive Debug
print("\n" + "=" * 60)
print("COMPREHENSIVE DEBUG")
print("=" * 60)

from backend.nlp.intent_extractor import load_model, tokenizer, model, alias_map, DEPARTMENTS
from fuzzywuzzy import process, fuzz

load_model()

test = "Cardiology doctors tomorrow"
test_lower = test.lower()

print(f"Query: '{test}'")
print(f"Query lowercase: '{test_lower}'")
print(f"\n1. Checking gazetteer (alias_map):")
print(f"   Alias map size: {len(alias_map)}")
print(f"   Sample aliases: {list(alias_map.items())[:5]}")

for alias, official in alias_map.items():
    if alias in test_lower:
        print(f"   ✅ Found in gazetteer: '{alias}' → '{official}'")

print(f"\n2. Checking fuzzy match:")
print(f"   DEPARTMENTS list: {DEPARTMENTS[:5]}...")
match, score = process.extractOne(
    test,
    DEPARTMENTS,
    scorer=fuzz.token_sort_ratio
)
print(f"   Best match: '{match}' (score: {score})")
print(f"   Threshold: 75, Result: {'PASS' if score >= 75 else 'FAIL'}")

print(f"\n3. Checking if symptom query:")
from backend.nlp.symptom_triage import is_symptom_query
print(f"   Is symptom: {is_symptom_query(test)}")