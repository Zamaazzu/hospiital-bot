# test_nlp_queries.py — run from project root: python test_nlp_queries.py

from backend.nlp.intent_extractor import extract_intent_slots, load_model
from backend.nlp.intent_adapter import adapt_intent_result

print("Loading model...")
if not load_model():
    print("Model failed to load. Check models/intent_classifier/ exists.")
    exit(1)

# Each entry: (query, expected_intent or None, expected_department or None)
# expected = None means "no strong expectation, just log the output for review"

test_cases = [

    # ── CRITICAL REGRESSION: "op" substring bug ────────────────
    # These department names contain "op" as a substring and should
    # NOT get misrouted to op_enquiry because of the new
    # `if "op" in text_lower` check.
    ("Orthopaedics doctor available tomorrow", "doctor_availability", "Orthopaedics"),
    ("Orthopaedics doctors today",             "doctor_availability", "Orthopaedics"),
    ("Is there an Orthopaedics doctor",        "doctor_availability", "Orthopaedics"),
    ("Book a token for Orthopaedics",          "token_booking",       "Orthopaedics"),

    # ── CRITICAL REGRESSION: "ENT" short-code substring risk ───
    # "ENT" can falsely match inside words like "different", "urgent", "patient"
    ("Is my token confirmed, I am a patient here", "token_status", None),
    ("This is urgent, doctor undo",                 None, None),  # log only, ambiguous
    ("ENT doctors today",                            "doctor_availability", "ENT"),
    ("ENT doctor available tomorrow",                "doctor_availability", "ENT"),

    # ── Original bug case — should now be fixed ────────────────
    ("Cardiology doctors tomorrow",              "doctor_availability", "Cardiology"),
    ("Doctors available in Cardiology tomorrow", "doctor_availability", "Cardiology"),
    ("Show me Cardiology doctors",               "doctor_availability", "Cardiology"),
    ("Is there a Cardiology doctor available",   "doctor_availability", "Cardiology"),
    ("List doctors in Neurology today",          "doctor_availability", "Neurology"),

    # ── Plain English, other departments ────────────────────────
    ("Any doctors in Dermatology",               "doctor_availability", "Dermatology"),
    ("Gastroenterology doctor available",        "doctor_availability", "Gastroenterology"),

    # ── Minimal extra words ─────────────────────────────────────
    ("Cardiology",       None, "Cardiology"),
    ("Cardiology today", None, "Cardiology"),
    ("Cardiology tomorrow", None, "Cardiology"),

    # ── doctor_availability without department ──────────────────
    ("Is any doctor available today", "doctor_availability", None),
    ("Doctor available now",          "doctor_availability", None),

    # ── token_booking, plain English ─────────────────────────────
    ("Book a token for Cardiology",              "token_booking", "Cardiology"),
    ("I want to book an appointment tomorrow",   "token_booking", None),
    ("Book me a slot with a Cardiology doctor",  "token_booking", "Cardiology"),

    # ── op_enquiry — genuine "OP" as a standalone word ───────────
    ("What are your OP timings",     "op_enquiry", None),
    ("Is the hospital open today",   "op_enquiry", None),
    ("What departments do you have", "op_enquiry", None),
    ("Is OP available today",        "op_enquiry", None),
    ("OP timing?",                   "op_enquiry", None),

    # ── token_status, plain English ──────────────────────────────
    ("What is the status of my token", "token_status", None),
    ("Check my token number",          "token_status", None),
    ("Has my token been called",       "token_status", None),
    ("How many people are ahead of me","token_status", None),

    # ── symptom-based ────────────────────────────────────────────
    ("I have chest pain",                     None, "Cardiology"),
    ("My knee hurts, is a doctor available",  "doctor_availability", "Orthopaedics"),
    ("enikku nenju vedana undu",              "token_booking", "Cardiology"),

    # ── Malayalam / code-mixed (spot-check, not exhaustive) ──────
    ("Cardiology OP undo?",        "op_enquiry", "Cardiology"),
    ("Dr. John today available?",  "doctor_availability", None),
    ("Token cancel cheyyanam",     "cancel_token", None),

    # ── Edge cases ────────────────────────────────────────────────
    ("",      None, None),   # empty string
    ("   ",   None, None),   # whitespace only
    ("asdkfj alskdjf laksjdf", "unclear", None),  # gibberish
    ("CAR-20260710-001",       None, None),        # bare token number, no verb
]

print("=" * 70)
print("NLP REGRESSION + COVERAGE TEST")
print("=" * 70)

pass_count = 0
fail_count = 0
review_count = 0

failures = []

for query, expected_intent, expected_dept in test_cases:
    try:
        extracted = extract_intent_slots(query)
    except Exception as e:
        print(f"\n💥 CRASH on query: {query!r}")
        print(f"   Exception: {e}")
        fail_count += 1
        failures.append((query, expected_intent, "CRASH", str(e)))
        continue

    intent = extracted.get("intent")
    slots = extracted.get("slots", {})
    department = slots.get("department")
    confidence = extracted.get("confidence")

    intent_ok = (expected_intent is None) or (intent == expected_intent)
    dept_ok = (expected_dept is None) or (department == expected_dept)

    if expected_intent is None and expected_dept is None:
        status = "ℹ️  REVIEW"
        review_count += 1
    elif intent_ok and dept_ok:
        status = "✅ PASS"
        pass_count += 1
    else:
        status = "❌ FAIL"
        fail_count += 1
        failures.append((query, expected_intent, intent, f"dept expected={expected_dept} got={department}"))

    print(f"\n{status}  Query: {query!r}")
    print(f"   Intent: {intent} (expected: {expected_intent}) | confidence: {confidence}")
    print(f"   Department: {department} (expected: {expected_dept})")
    print(f"   Full slots: {slots}")

print("\n" + "=" * 70)
print(f"PASS: {pass_count}  FAIL: {fail_count}  REVIEW-ONLY: {review_count}  TOTAL: {len(test_cases)}")
print("=" * 70)

if failures:
    print("\n--- FAILED CASES (send these to Person 3) ---")
    for query, expected, got, note in failures:
        print(f"❌ '{query}'")
        print(f"   Expected intent: {expected} | Got: {got}")
        print(f"   {note}\n")
else:
    print("\nNo hard failures. Review the ℹ️ REVIEW lines manually for sanity.")