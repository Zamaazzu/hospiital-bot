import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.nlp.intent_extractor import load_model, extract_intent_slots

load_model()


# ==========================================================
# MALAYALAM STRESS TEST
# ==========================================================

test_queries = [

    # ---------------- BOOKING ----------------
    ("എനിക്ക് ടോക്കൺ വേണം", "token_booking"),
    ("എനിക്ക് ഒരു ടോക്കൺ ബുക്ക് ചെയ്യണം", "token_booking"),
    ("കാർഡിയോളജി വിഭാഗത്തിൽ ടോക്കൺ വേണം", "token_booking"),
    ("എനിക്ക് ഹൃദയ ഡോക്ടറെ കാണണം", "token_booking"),
    ("എനിക്ക് കണ്ണ് ഡോക്ടറെ കാണണം", "token_booking"),
    ("എനിക്ക് ചെവി ഡോക്ടറെ കാണണം", "token_booking"),
    ("എനിക്ക് വയർ ഡോക്ടറെ കാണണം", "token_booking"),
    ("എനിക്ക് ന്യൂറോളജി ഡോക്ടറെ കാണണം", "token_booking"),
    ("ഓർത്തോപീഡിക്സ് ഡോക്ടറെ ബുക്ക് ചെയ്യുക", "token_booking"),
    ("ഡെർമറ്റോളജി ഡോക്ടറെ ബുക്ക് ചെയ്യണം", "token_booking"),
    ("നാളെ ടോക്കൺ ബുക്ക് ചെയ്യണം", "token_booking"),
    ("ഇന്ന് ഒരു ഡോക്ടറെ കാണണം", "token_booking"),

    # ---------------- DOCTOR AVAILABILITY ----------------
    ("ഇന്ന് കാർഡിയോളജി ഡോക്ടർ ഉണ്ടോ", "doctor_availability"),
    ("നാളെ ന്യൂറോളജി ഡോക്ടർ ഉണ്ടോ", "doctor_availability"),
    ("ഇന്ന് ഡെർമറ്റോളജി ഡോക്ടർ ഉണ്ടോ", "doctor_availability"),
    ("കണ്ണ് ഡോക്ടർ ഇന്ന് ഉണ്ടോ", "doctor_availability"),
    ("ചെവി ഡോക്ടർ ഇന്ന് ഉണ്ടോ", "doctor_availability"),
    ("ഹൃദയ ഡോക്ടർ ഇന്ന് ഉണ്ടോ", "doctor_availability"),
    ("ഓർത്തോപീഡിക്സ് ഡോക്ടർ ലഭ്യമാണോ", "doctor_availability"),
    ("ഇന്ന് ഡോക്ടർ ഫ്രീ ആണോ", "doctor_availability"),
    ("കാർഡിയോളജി ഡോക്ടർ ലഭ്യമാണോ", "doctor_availability"),

    # ---------------- OP ----------------
    ("ഇന്ന് ഒ.പി ഉണ്ടോ", "op_enquiry"),
    ("ഒ.പി സമയം എന്താണ്", "op_enquiry"),
    ("ഒ.പി എപ്പോഴാണ് തുടങ്ങുന്നത്", "op_enquiry"),
    ("ഒ.പി എത്ര മണിക്ക് തുറക്കും", "op_enquiry"),
    ("ഇന്ന് ഒ.പി പ്രവർത്തിക്കുന്നുണ്ടോ", "op_enquiry"),
    ("നാളെ ഒ.പി ഉണ്ടോ", "op_enquiry"),

    # ---------------- STATUS ----------------
    ("എന്റെ ടോക്കൺ നമ്പർ എന്താണ്", "token_status"),
    ("എന്റെ ടോക്കൺ എത്തിയോ", "token_status"),
    ("എന്റെ ടോക്കൺ സ്ഥിതി പറയൂ", "token_status"),
    ("ഇനി എത്ര പേർ ബാക്കിയുണ്ട്", "token_status"),
    ("എന്റെ നമ്പർ എപ്പോഴാണ് വരുന്നത്", "token_status"),

    # ---------------- CANCEL ----------------
    ("എന്റെ ടോക്കൺ റദ്ദാക്കണം", "cancel_token"),
    ("ബുക്ക് ചെയ്ത ടോക്കൺ ഒഴിവാക്കണം", "cancel_token"),
    ("എനിക്ക് ടോക്കൺ വേണ്ട", "cancel_token"),
    ("അപ്പോയിന്റ്മെന്റ് റദ്ദാക്കണം", "cancel_token"),
    ("ബുക്കിംഗ് റദ്ദാക്കുക", "cancel_token"),

    # ---------------- SYMPTOMS ----------------
    ("എനിക്ക് നെഞ്ചുവേദനയുണ്ട്", "token_booking"),
    ("എനിക്ക് തലവേദനയുണ്ട്", "token_booking"),
    ("എനിക്ക് വയറുവേദനയുണ്ട്", "token_booking"),
    ("എനിക്ക് കണ്ണിന് വേദനയുണ്ട്", "token_booking"),
    ("എനിക്ക് ചെവി വേദനയുണ്ട്", "token_booking"),
    ("എനിക്ക് പനിയുണ്ട്", "token_booking"),
    ("എനിക്ക് ശ്വാസതടസ്സമുണ്ട്", "token_booking"),
    ("എനിക്ക് തൊലിയിൽ ചൊറിച്ചിലുണ്ട്", "token_booking"),
    ("എനിക്ക് മുട്ടുവേദനയുണ്ട്", "token_booking"),
    ("എനിക്ക് വൃക്ക വേദനയുണ്ട്", "token_booking"),

    # ---------------- AMBIGUOUS ----------------
    ("ഡോക്ടർ", "unclear"),
    ("ടോക്കൺ", "unclear"),
    ("കാർഡിയോളജി", "unclear"),
    ("ഹൃദയം", "unclear"),
    ("ഒ.പി", "op_enquiry"),

    # ---------------- GARBAGE ----------------
    ("asdfasdf", "unclear"),
    ("......", "unclear"),
    ("12345", "unclear"),
    ("@@@###", "unclear"),
]


correct = 0

print("=" * 70)
print("MALAYALAM NLP STRESS TEST")
print("=" * 70)

for query, expected in test_queries:

    result = extract_intent_slots(query)

    intent = result["intent"]

    if intent == expected:
        status = "✅"
        correct += 1
    else:
        status = "❌"

    print(f"\n{status} {query}")
    print(f"Expected : {expected}")
    print(f"Predicted: {intent}")
    print(f"Confidence: {result['confidence']}")
    print(f"Slots: {result['slots']}")

print("\n" + "=" * 70)
print(f"Accuracy : {correct}/{len(test_queries)} = {correct/len(test_queries)*100:.2f}%")
print("=" * 70)