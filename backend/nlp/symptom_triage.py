SYMPTOM_MAP = {
    "chest pain": "Cardiology",
    "heart pain": "Cardiology",
    "nenju vedana": "Cardiology",

    "fever": "Physician",
    "pani": "Physician",

    "eye pain": "Ophthalmology",
    "kannu vedana": "Ophthalmology",

    "ear pain": "ENT",
    "chevi vedana": "ENT",

    "bone pain": "Orthopedics",
    "ellu vedana": "Orthopedics",

    "skin rash": "Dermatology",
    "itching": "Dermatology",

    "stomach pain": "Gastroenterology",
    "vayar vedana": "Gastroenterology",

    "child": "Pediatrics",
    "kutti": "Pediatrics"
}

def symptom_triage(text: str) -> str:
    text = text.lower()
    for keyword, department in SYMPTOM_MAP.items():
        if keyword in text:
            return department
    return "General Medicine"