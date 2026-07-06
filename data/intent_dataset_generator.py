import json

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
# Templates
# ---------------------------------

op_enquiry_templates = [
    "{hospital} OP undo?",
    "{department} OP undo?",
    "{department} OP time?",
    "{hospital} il {department} OP eppozha?",
    "{hospital} today OP?",
    "{department} department open ano?"
]

doctor_availability_templates = [
    "{doctor} available ano?",
    "{doctor} innu undo?",
    "{doctor} nale undo?",
    "{doctor} OP undo?",
    "{doctor} today available?",
    "{doctor} working ano?"
]

token_booking_templates = [
    "{department} token venam",
    "{doctor} token book cheyyanam",
    "{hospital} token venam",
    "{doctor} appointment venam",
    "{department} OP token venam",
    "Book token for {doctor}"
]

token_status_templates = [
    "Ente token status",
    "Token number ethra?",
    "Token status parayu",
    "Check my token",
    "Current token?",
    "Token evide ethi?"
]

cancel_templates = [
    "Token cancel cheyyanam",
    "Cancel my token",
    "Booking cancel",
    "Appointment cancel",
    "Ente token cancel cheyyu"
]

# ---------------------------------
# Generate Dataset
# ---------------------------------

for hospital in hospitals:
    for template in op_enquiry_templates:
        dataset.append({
            "text": template.format(hospital=hospital, department="General Medicine"),
            "intent": "op_enquiry"
        })

for department in departments:
    for template in op_enquiry_templates:
        dataset.append({
            "text": template.format(
                hospital=hospitals[0],
                department=department
            ),
            "intent": "op_enquiry"
        })

for doctor in doctors:
    for template in doctor_availability_templates:
        dataset.append({
            "text": template.format(doctor=doctor),
            "intent": "doctor_availability"
        })

for doctor in doctors:
    for template in token_booking_templates:
        dataset.append({
            "text": template.format(
                doctor=doctor,
                department="General Medicine",
                hospital=hospitals[0]
            ),
            "intent": "token_booking"
        })

for template in token_status_templates:
    dataset.append({
        "text": template,
        "intent": "token_status"
    })

for template in cancel_templates:
    dataset.append({
        "text": template,
        "intent": "cancel_token"
    })

# Remove duplicates
unique = []
seen = set()

for item in dataset:
    key = (item["text"], item["intent"])
    if key not in seen:
        seen.add(key)
        unique.append(item)

# Save JSON
with open(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\intent_dataset.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(unique, f, indent=4, ensure_ascii=False)

print("Dataset created successfully!")
print("Total samples:", len(unique))