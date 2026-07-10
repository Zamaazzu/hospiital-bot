import json
import os
import random

from backend.db.database import SessionLocal
from backend.db.models import Hospital, Department, Doctor

db = SessionLocal()

# -------------------------------
# Read data from MySQL
# -------------------------------

hospitals = [h.name for h in db.query(Hospital).all()]
departments = [d.dept_name for d in db.query(Department).all()]
doctors = [d.doctor_name for d in db.query(Doctor).all()]

db.close()

dataset = []

# ---------------------------------
# Vocabulary (single source of truth — no duplicate defs)
# ---------------------------------

days = [
    "today", "tomorrow",
    "innu", "nale",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "this week", "next week"
]

time_of_day = [
    "morning", "afternoon", "evening", "night",
    "ravile", "uchakku", "vaikunneram", "raatri"
]

polite_words = [
    "please", "kindly", "can you", "could you", "would you", "if possible"
]

question_words = [
    "what", "when", "which", "can", "could", "please", "how"
]

urgency_words = [
    "immediately", "urgent", "as soon as possible", "ippol", "vegam", "today itself"
]

confirmation_words = [
    "confirm", "confirmed", "verify", "check", "status"
]

# ---------------------------------
# Templates: token_booking
# ---------------------------------

token_booking_english = [
    "Book an appointment with {doctor}",
    "Book a token for {doctor}",
    "I need an appointment with {doctor}",
    "I want to consult {doctor}",
    "Can I book a token for {doctor}?",
    "Please book my appointment",
    "Book OP for {department}",
    "Need an appointment in {department}",
    "Schedule an appointment for {doctor}",
    "Reserve a token for {doctor}"
]

token_booking_malayalam = [
    "{doctor} നെ കാണണം",
    "{department} ൽ ടോക്കൺ വേണം",
    "ഒരു ടോക്കൺ ബുക്ക് ചെയ്യണം",
    "അപ്പോയിന്റ്മെന്റ് വേണം",
    "ഡോക്ടറെ കാണാൻ ടോക്കൺ വേണം",
    "ഇന്നത്തേക്ക് ടോക്കൺ വേണം",
    "നാളത്തേക്ക് ടോക്കൺ വേണം",
    "ഡോക്ടറുടെ അപ്പോയിന്റ്മെന്റ് വേണം",
    "ഒ.പി ടോക്കൺ വേണം",
    "ബുക്ക് ചെയ്ത് തരാമോ?"
]

token_booking_codemix = [
    "{doctor} token venam",
    "{doctor} appointment venam",
    "{department} OP token venam",
    "Book cheyyanam for {doctor}",
    "{doctor} available aanenkil book cheyyu",
    "{department} booking venam",
    "Token book cheyyanam",
    "Appointment book cheyyu",
    "Doctor appointment venam",
    "OP booking cheyyanam"
]

token_booking_short = [
    "book token",
    "appointment",
    "token",
    "booking",
    "{doctor}",
    "{department}",
    "{doctor} token",
    "{department} booking",
    "OP booking",
    "book"
]

token_booking_extra = [
    "{polite} book a token for {doctor} {day} {time}",
    "I want to book {doctor} for {day} {time}",
    "Book me an OP slot in {department} for {day}",
    "{doctor} kku {day} {time} token venam",
    "{department} il {day} appointment venam",
    "{polite} reserve {doctor}'s OP for {day}",
    "Need a {urgency} appointment with {doctor}",
    "{department} OP {day} token book cheyyanam",
    "Can you {confirm} and book my token for {doctor}?",
    "Book {doctor} appointment for {time} {day}",
    "{polite} arrange a token in {department} {time}",
    "I need to see {doctor} {day} {time}, book it"
]

# ---------------------------------
# Templates: op_enquiry
# ---------------------------------

op_enquiry_english = [
    "Is OP available in {department}?",
    "What is the OP timing for {department}?",
    "When is the OP for {department}?",
    "Does {hospital} have OP today?",
    "Is {department} open today?",
    "What are today's OP hours?",
    "Can I visit {department} today?",
    "Is consultation available in {department}?",
    "What time does OP start?",
    "What time does OP end?",
    "Is OP open tomorrow?",
    "What are the OP timings at {hospital}?",
    "Which departments have OP today?",
    "Is {department} functioning today?",
    "Can I consult a doctor in {department} today?"
]

op_enquiry_malayalam = [
    "{department} ഒ.പി ഉണ്ടോ?",
    "{department} ഒ.പി എപ്പോഴാണ്?",
    "{hospital} ൽ ഒ.പി ഉണ്ടോ?",
    "ഇന്ന് ഒ.പി ഉണ്ടോ?",
    "നാളെ ഒ.പി ഉണ്ടോ?",
    "{department} ഇന്ന് തുറന്നിട്ടുണ്ടോ?",
    "ഒ.പി സമയം എന്താണ്?",
    "ഡോക്ടറെ കാണാൻ എപ്പോൾ വരണം?",
    "കൺസൾട്ടേഷൻ സമയം എന്താണ്?",
    "ഒ.പി രാവിലെ ആണോ?",
    "ഒ.പി വൈകുന്നേരം ആണോ?",
    "{department} ഡോക്ടർ ഇന്ന് ഉണ്ടോ?",
    "ഒ.പി എപ്പോൾ തുടങ്ങും?",
    "ഒ.പി എപ്പോൾ അവസാനിക്കും?",
    "ഇന്ന് ആശുപത്രിയിൽ ഒ.പി ഉണ്ടോ?"
]

op_enquiry_codemix = [
    "{department} OP undo?",
    "{department} OP time entha?",
    "{hospital} OP undo?",
    "{department} today open ano?",
    "OP timing parayamo?",
    "{department} consultation time?",
    "Doctor OP today?",
    "Hospital OP available ano?",
    "OP ravile ano?",
    "OP evening undo?",
    "{department} OP schedule?",
    "Innu OP undo?",
    "Nale OP undo?",
    "{department} doctor available ano?",
    "OP start time?"
]

op_enquiry_short = [
    "OP",
    "OP time",
    "OP today",
    "OP tomorrow",
    "{department}",
    "{department} OP",
    "{hospital}",
    "hospital OP",
    "consultation",
    "doctor timing"
]

op_enquiry_extra = [
    "Is OP available in {department} on {day}?",
    "What is the {department} OP timing on {day} {time}?",
    "{polite} tell me the OP schedule for {department}",
    "Is {hospital} OP open in the {time}?",
    "Can I visit {department} {day} {time}?",
    "{department} OP {day} undo?",
    "{department} OP {day} {time} time entha?",
    "{polite} check OP availability for {department}",
    "Is there an {urgency} OP slot in {department}?",
    "{department} OP {confirm} cheyyamo?",
    "{question} time does {department} OP start on {day}?",
    "{hospital} {department} OP {day} {time} undo?"
]

# ---------------------------------
# Templates: doctor_availability
# ---------------------------------

doctor_availability_english = [
    "Is {doctor} available today?",
    "Is {doctor} on duty?",
    "Can I meet {doctor} today?",
    "When is {doctor} available?",
    "Does {doctor} have OP today?",
    "Is {doctor} working tomorrow?",
    "Can I consult {doctor}?",
    "Is {doctor} available this evening?",
    "Is {doctor} available this morning?",
    "Which day is {doctor} available?",
    "Can I see {doctor} today?",
    "Is {doctor} in the hospital?",
    "Is {doctor} consulting today?",
    "Does {doctor} have appointments today?",
    "When can I meet {doctor}?"
]

doctor_availability_malayalam = [
    "{doctor} ഇന്ന് ഉണ്ടോ?",
    "{doctor} നാളെ ഉണ്ടോ?",
    "{doctor} ഡ്യൂട്ടിയിലാണോ?",
    "{doctor} നെ ഇന്ന് കാണാമോ?",
    "{doctor} എപ്പോൾ ഉണ്ടാകും?",
    "{doctor} ഒ.പി ഉണ്ടോ?",
    "{doctor} ഇന്ന് കൺസൾട്ട് ചെയ്യുമോ?",
    "{doctor} രാവിലെ ഉണ്ടോ?",
    "{doctor} വൈകുന്നേരം ഉണ്ടോ?",
    "{doctor} ഏത് ദിവസമാണ് ഉണ്ടാകുന്നത്?",
    "ഡോക്ടർ ഇന്ന് ആശുപത്രിയിലുണ്ടോ?",
    "{doctor} ഇന്ന് വരുമോ?",
    "{doctor} ഇന്ന് കാണാൻ പറ്റുമോ?",
    "{doctor} ലഭ്യമാണോ?",
    "{doctor} എപ്പോഴാണ് കാണാൻ കഴിയുക?"
]

doctor_availability_codemix = [
    "{doctor} available ano?",
    "{doctor} innu undo?",
    "{doctor} nale undo?",
    "{doctor} OP undo?",
    "{doctor} working ano?",
    "{doctor} today available?",
    "{doctor} duty il ano?",
    "Doctor available today?",
    "{doctor} consultation undo?",
    "{doctor} hospital il undo?",
    "{doctor} evening available?",
    "{doctor} morning undo?",
    "{doctor} meet cheyyan pattumo?",
    "{doctor} leave ano?",
    "{doctor} free ano?"
]

doctor_availability_short = [
    "{doctor}",
    "{doctor} today",
    "{doctor} available",
    "{doctor} OP",
    "doctor",
    "doctor today",
    "available",
    "consultation",
    "duty",
    "doctor timing"
]

doctor_availability_extra = [
    "Is {doctor} available on {day} {time}?",
    "{polite} tell me if {doctor} is free {day}",
    "{doctor} {day} {time} undo?",
    "Can I {confirm} {doctor}'s availability for {day}?",
    "{doctor} is available in the {time} on {day}?",
    "{question} day is {doctor} on duty in {department}?",
    "I need to meet {doctor} {urgency}, is that possible?",
    "{doctor} {department} il {day} undo?",
    "{polite} check {doctor} availability {time}",
    "Is {doctor} at {hospital} {day} {time}?"
]

# ---------------------------------
# Templates: token_status
# ---------------------------------

token_status_english = [
    "Check my token",
    "What is my token number?",
    "What is my token status?",
    "Has my token been confirmed?",
    "Is my token active?",
    "When is my turn?",
    "How many patients are ahead of me?",
    "What is the current token?",
    "Check appointment status",
    "Is my booking confirmed?",
    "Where is my token now?",
    "What token is being served?",
    "Has my token been called?",
    "How long is the waiting time?",
    "Can you check my appointment?"
]

token_status_malayalam = [
    "എന്റെ ടോക്കൺ സ്റ്റാറ്റസ് എന്താണ്?",
    "എന്റെ ടോക്കൺ നമ്പർ എന്താണ്?",
    "ടോക്കൺ എവിടെ എത്തി?",
    "എന്റെ ടേൺ എപ്പോഴാണ്?",
    "ടോക്കൺ കൺഫേം ആയോ?",
    "ഇപ്പോൾ ഏത് ടോക്കൺ ആണ്?",
    "വെയിറ്റിംഗ് എത്രയാണ്?",
    "എന്റെ അപ്പോയിന്റ്മെന്റ് സ്റ്റാറ്റസ്?",
    "ടോക്കൺ പരിശോധിക്കൂ",
    "ടോക്കൺ വിവരം പറയൂ",
    "എന്റെ ബുക്കിംഗ് ശരിയായോ?",
    "എത്ര പേർ ബാക്കിയുണ്ട്?",
    "ടോക്കൺ വിളിച്ചോ?",
    "സ്റ്റാറ്റസ് അറിയണം",
    "ടോക്കൺ നമ്പർ പറയൂ"
]

token_status_codemix = [
    "Token status",
    "Check my token",
    "Current token?",
    "Token evide ethi?",
    "Ente token status",
    "Token number entha?",
    "Booking confirmed ano?",
    "Current token number?",
    "Appointment status",
    "Token waiting time?",
    "Token call cheytho?",
    "Ente turn eppo?",
    "Status parayamo?",
    "Token ready ano?",
    "Token check cheyyu"
]

token_status_short = [
    "token",
    "status",
    "token status",
    "current token",
    "my token",
    "booking status",
    "appointment status",
    "waiting",
    "turn",
    "token number"
]

token_status_extra = [
    "{polite} check my token status for {doctor}",
    "Is my {day} token with {doctor} {confirm}ed?",
    "{doctor} token status entha?",
    "{question} is my turn for {doctor} today?",
    "{polite} {confirm} my booking with {doctor}",
    "Ente {doctor} token status entha?",
    "How many people are ahead of me for {doctor}?",
    "Token status {department} {day}",
    "{polite} check waiting time in {department}",
    "Is my {day} {time} appointment {confirm}ed?"
]

# ---------------------------------
# Templates: cancel_token
# ---------------------------------

cancel_token_english = [
    "Cancel my token",
    "Cancel my appointment",
    "I want to cancel my booking",
    "Please cancel my token",
    "Delete my appointment",
    "Remove my booking",
    "Cancel today's appointment",
    "Cancel tomorrow's booking",
    "I don't need the appointment",
    "Cancel OP booking",
    "Withdraw my token",
    "Cancel consultation",
    "Stop my appointment",
    "Cancel the reservation",
    "I want to reschedule later"
]

cancel_token_malayalam = [
    "എന്റെ ടോക്കൺ റദ്ദാക്കൂ",
    "അപ്പോയിന്റ്മെന്റ് റദ്ദാക്കണം",
    "ബുക്കിംഗ് റദ്ദാക്കൂ",
    "ടോക്കൺ വേണ്ട",
    "ഇന്നത്തെ ടോക്കൺ റദ്ദാക്കൂ",
    "നാളത്തെ ടോക്കൺ റദ്ദാക്കൂ",
    "ഒ.പി റദ്ദാക്കണം",
    "ഡോക്ടറെ ഇനി കാണേണ്ട",
    "എന്റെ ബുക്കിംഗ് ഒഴിവാക്കൂ",
    "റദ്ദാക്കാൻ സഹായിക്കൂ",
    "അപ്പോയിന്റ്മെന്റ് ഒഴിവാക്കൂ",
    "ടോക്കൺ ക്യാൻസൽ ചെയ്യണം",
    "എനിക്ക് വരാൻ പറ്റില്ല",
    "ടോക്കൺ ഡിലീറ്റ് ചെയ്യൂ",
    "ബുക്കിംഗ് വേണ്ട"
]

cancel_token_codemix = [
    "Cancel my token",
    "Token cancel cheyyanam",
    "Appointment cancel cheyyu",
    "Booking cancel",
    "Token venda",
    "Cancel booking please",
    "OP cancel",
    "Appointment venda",
    "Booking remove cheyyu",
    "Cancel today's token",
    "Nale token cancel",
    "Token delete cheyyu",
    "Appointment remove",
    "Cancel consultation",
    "Booking cancel cheyyanam"
]

cancel_token_short = [
    "cancel",
    "cancel token",
    "cancel booking",
    "appointment cancel",
    "token venda",
    "delete booking",
    "remove token",
    "cancel OP",
    "booking",
    "token cancel"
]

cancel_token_extra = [
    "{polite} cancel my token for {doctor} on {day}",
    "{doctor} {day} appointment cancel cheyyanam",
    "I want to cancel my {day} {time} booking",
    "{polite} cancel my {department} OP token",
    "Cancel my token with {doctor}, {urgency}",
    "{department} {day} booking cancel cheyyu",
    "{polite} remove my {day} appointment with {doctor}",
    "Ente {doctor} token {day} cancel cheyyanam",
    "Can you {confirm} the cancellation of my {doctor} token?",
    "Cancel {doctor} {time} appointment {day}"
]

# ---------------------------------
# Generate Dataset
# ---------------------------------

random.seed(42)

TARGET_PER_INTENT = 400  # 5 intents x 400 = ~2000 samples
MAX_ATTEMPTS = 20000


def generate_unique_samples(intent, template_groups):

    generated = set()
    attempts = 0

    while len(generated) < TARGET_PER_INTENT and attempts < MAX_ATTEMPTS:

        attempts += 1

        template = random.choice(random.choice(template_groups))

        values = {
            "hospital": random.choice(hospitals),
            "department": random.choice(departments),
            "doctor": random.choice(doctors),
            "day": random.choice(days),
            "time": random.choice(time_of_day),
            "polite": random.choice(polite_words),
            "question": random.choice(question_words),
            "urgency": random.choice(urgency_words),
            "confirm": random.choice(confirmation_words),
        }

        try:
            sentence = template.format(**values).strip()
        except KeyError:
            continue

        key = sentence.lower()

        if key in generated:
            continue

        generated.add(key)

        dataset.append({
            "text": sentence,
            "intent": intent
        })

    print(f"{intent}: {len(generated)} samples")


generate_unique_samples(
    "op_enquiry",
    [
        op_enquiry_english,
        op_enquiry_malayalam,
        op_enquiry_codemix,
        op_enquiry_short,
        op_enquiry_extra
    ]
)

generate_unique_samples(
    "doctor_availability",
    [
        doctor_availability_english,
        doctor_availability_malayalam,
        doctor_availability_codemix,
        doctor_availability_short,
        doctor_availability_extra
    ]
)

generate_unique_samples(
    "token_booking",
    [
        token_booking_english,
        token_booking_malayalam,
        token_booking_codemix,
        token_booking_short,
        token_booking_extra
    ]
)

generate_unique_samples(
    "token_status",
    [
        token_status_english,
        token_status_malayalam,
        token_status_codemix,
        token_status_short,
        token_status_extra
    ]
)

generate_unique_samples(
    "cancel_token",
    [
        cancel_token_english,
        cancel_token_malayalam,
        cancel_token_codemix,
        cancel_token_short,
        cancel_token_extra
    ]
)

# ---------------------------------
# Final Cleanup
# ---------------------------------

random.shuffle(dataset)

print("Total samples:", len(dataset))

# ---------------------------------
# Save JSON (portable path — saves next to this script, in data/)
# ---------------------------------

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "intent_dataset.json")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print(f"Dataset created successfully at {OUTPUT_PATH}")
print("Total samples:", len(dataset))