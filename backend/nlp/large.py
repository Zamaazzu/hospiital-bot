from intent_extractor import load_model, extract_intent_slots

# Load model
load_model()

# ----------------------------------------------------
# TEST DATA
# Add as many queries as you want.
# Format:
# ("query", "expected_intent")
# ----------------------------------------------------

TEST_QUERIES = [

# ===========================
# OP ENQUIRY
# ===========================

("OP undo?", "op_enquiry"),
("OP timing?", "op_enquiry"),
("Cardiology OP undo?", "op_enquiry"),
("ENT OP undo?", "op_enquiry"),
("Neurology OP today?", "op_enquiry"),
("Hospital OP today?", "op_enquiry"),
("ഇന്ന് ഒ.പി ഉണ്ടോ?", "op_enquiry"),
("What time does OP start?", "op_enquiry"),
("Morning OP undo?", "op_enquiry"),
("General Medicine OP?", "op_enquiry"),

# ===========================
# DOCTOR AVAILABILITY
# ===========================

("Doctor undo?", "doctor_availability"),
("Dr Rahul undo?", "doctor_availability"),
("Dr Priya available?", "doctor_availability"),
("Doctor free ano?", "doctor_availability"),
("Who is available today?", "doctor_availability"),
("ഇന്ന് ഡോക്ടർ ഉണ്ടോ?", "doctor_availability"),
("Doctor nale undo?", "doctor_availability"),
("Is Dr John working?", "doctor_availability"),
("Can I meet doctor?", "doctor_availability"),
("Available doctor?", "doctor_availability"),

# ===========================
# TOKEN BOOKING
# ===========================

("Doctorine Kananam", "token_booking"),
("Book token", "token_booking"),
("Appointment venam", "token_booking"),
("Need appointment", "token_booking"),
("Reserve token", "token_booking"),
("Slot book cheyyanam", "token_booking"),
("Doctor appointment venam", "token_booking"),
("Book cardiology", "token_booking"),
("OP token venam", "token_booking"),
("Book me a slot", "token_booking"),

# ===========================
# TOKEN STATUS
# ===========================

("Token status", "token_status"),
("Current token?", "token_status"),
("Token number?", "token_status"),
("Ente token evide?", "token_status"),
("Booking confirmed?", "token_status"),
("Current queue?", "token_status"),
("How many before me?", "token_status"),
("Status parayu", "token_status"),
("Token confirm ayo?", "token_status"),
("Appointment status?", "token_status"),

# ===========================
# CANCEL TOKEN
# ===========================

("Cancel token", "cancel_token"),
("Cancel appointment", "cancel_token"),
("Booking cancel", "cancel_token"),
("Token venda", "cancel_token"),
("Appointment venda", "cancel_token"),
("Please cancel", "cancel_token"),
("Remove booking", "cancel_token"),
("Innu varan budhimuttu ond", "cancel_token"),
("Innu varan chance illa", "cancel_token"),
("Thalparym illa inn varan", "cancel_token"),
]

# ----------------------------------------------------
# TEST
# ----------------------------------------------------

correct = 0
wrong = []

print("="*70)
print("MuRIL Intent Classifier Test")
print("="*70)

for query, expected in TEST_QUERIES:

    result = extract_intent_slots(query)

    predicted = result["intent"]

    if predicted == expected:
        correct += 1
        icon = "✅"
    else:
        icon = "❌"
        wrong.append((query, expected, predicted))

    print(f"{icon} {query}")
    print(f"   Expected : {expected}")
    print(f"   Predicted: {predicted}")
    print()

accuracy = correct / len(TEST_QUERIES) * 100

print("="*70)
print("SUMMARY")
print("="*70)
print(f"Correct  : {correct}")
print(f"Wrong    : {len(TEST_QUERIES)-correct}")
print(f"Accuracy : {accuracy:.2f}%")

print("="*70)

if wrong:
    print("\nFAILED QUERIES\n")
    for query, expected, predicted in wrong:
        print(f"Query      : {query}")
        print(f"Expected   : {expected}")
        print(f"Predicted  : {predicted}")
        print("-"*50)
else:
    print("\n🎉 ALL TESTS PASSED!")

print("="*70)