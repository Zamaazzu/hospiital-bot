# backend/nlp/intent_extractor.py

import os
import re
import torch
from pathlib import Path
from fuzzywuzzy import process, fuzz
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .symptom_triage import symptom_triage, SYMPTOM_MAP, is_symptom_query

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models" / "intent_classifier"
GAZETTEER = BASE_DIR / "data" / "medical_terms_gazetteer.txt"

# ── Intent Labels (must match muril_train.py order exactly) ───
INTENT_LABELS = [
    "op_enquiry",
    "doctor_availability",
    "token_booking",
    "token_status",
    "cancel_token"
]

# ── Departments (exact names from DB) ─────────────────────────
DEPARTMENTS = [
    "Anaesthesiology",
    "Cancer Care",
    "Cardio Thoracic & Vascular Surgery",
    "Cardiology",
    "Child Development Centre",
    "Critical Care",
    "Dental Maxillofacial Surgery",
    "Dermatology",
    "ENT",
    "Emergency Medicine",
    "Gastroenterology",
    "Infertility & Laparoscopy",
    "Interventional Radiology",
    "Neonatology",
    "Nephrology",
    "Neurology",
    "Neurosurgery",
    "Obstetrics & Gynaecology",
    "Orthopaedics",
    "Paediatrics",
    "Physiotherapy",
    "Pulmanology",
    "Urology",
]

# ── Keyword Backup (used when model confidence is medium) ──────
KEYWORD_RULES = {
    "cancel_token": [
        "patilla", "kazhiyilla", "budhimuttu",
        "varan patilla", "varaan patilla",
        "pokaan patilla", "varaan kazhiyilla",
        "cancel", "withdraw", "remove booking",
        "venda", "venda ipo", "njan varaan patilla",
    ],
    "token_booking": [
        "venam", "veno", "book", "booking",
        "token venam", "appointment venam",
        "slot venam", "kanam", "kaanam",
        "edukkanam", "pokanam", "doctor kanam",
        "slot veno", "ravile slot", "tol vedana",
    ],
    "token_status": [
        "status", "turn", "eppo vilikum",
        "etra per", "waiting", "confirmed",
        "token number", "ente turn", "evide ethi",
        "token evide", "token call aayo","ethra per munnil","how many people ahead of me"
        "ippo vilikkuvo"
    ],
    "doctor_availability": [
        "doctor undo", "doctor und",
        "duty", "free", "doctor innu",
        "doctor nale", "doctor varmo",
        # removed generic "available" — too broad, caused false matches
    ],
    "op_enquiry": [
        "OP undo", "OP und", "OP timing",
        "OP schedule", "OP open", "OP nale",
        "OP innu", "enthu cheyyum", "OP?",
        "OP available", "is OP",
    ],
}

# ── Global Model Variables ────────────────────────────────────
tokenizer = None
model     = None
alias_map = {}

# ── Load Gazetteer ────────────────────────────────────────────
def load_gazetteer():
    global alias_map
    alias_map = {}

    if not GAZETTEER.exists():
        print(f"Gazetteer not found at {GAZETTEER} - skipping")
        return

    with open(GAZETTEER, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                alias, official = line.split("=", 1)
                alias_map[alias.strip().lower()] = official.strip()

    print(f"Gazetteer loaded: {len(alias_map)} aliases")

# ── Load Model ────────────────────────────────────────────────
def load_model():
    global tokenizer, model

    if not MODEL_DIR.exists():
        print(f"Model not found at {MODEL_DIR}. Run muril_train.py first.")
        return False

    print("Loading MuRIL model...")
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    model     = AutoModelForSequenceClassification.from_pretrained(
                    str(MODEL_DIR))
    model.eval()
    load_gazetteer()
    print("Model loaded successfully")
    return True

def extract_department(text: str) -> str | None:
    text_lower = text.lower()
    if len(text.strip()) <= 3:
        return None
    # 1. Symptom → Department
    if is_symptom_query(text):
        dept = symptom_triage(text)
        if dept:
            return dept

    # 2. Gazetteer aliases
    for alias, official in alias_map.items():
        if alias in text_lower:
            return official

    # 3. Exact department name match
    for dept in DEPARTMENTS:
        if dept.lower() in text_lower:
            return dept

    # 4. Fuzzy match only if nothing matched
    match, score = process.extractOne(
        text,
        DEPARTMENTS,
        scorer=fuzz.partial_ratio
    )

    if score >= 80:
        return match

    return None

# ── Doctor Name Extraction ────────────────────────────────────
def extract_doctor(text: str) -> str | None:
    # Require capital letter name right after Dr./Doctor
    pattern = r'\b(?:Dr\.?|Doctor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
    match   = re.search(pattern, text)  # removed IGNORECASE
    if match:
        name = match.group(1).strip()
        stop_words = ["nale", "innu", "today", "tomorrow", "morning",
                      "evening", "night", "ravile", "vaikunneram",
                      "uchakku", "raatri"]
        name_parts = [p for p in name.split() if p.lower() not in stop_words]
        return " ".join(name_parts) if name_parts else None
    return None

# ── Token Number Extraction ───────────────────────────────────
def extract_token_number(text: str) -> str | None:
    pattern = r'\b([A-Z]{2,4}-\d{6,8}-\d{2,4}|\d{1,4})\b'
    match   = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

# ── Date Extraction ───────────────────────────────────────────
def extract_date(text: str) -> str | None:
    text_lower = text.lower()

    date_words = {
        "innu"     : "today",
        "today"    : "today",
        "nale"     : "tomorrow",
        "tomorrow" : "tomorrow",
        "monday"   : "Monday",
        "tuesday"  : "Tuesday",
        "wednesday": "Wednesday",
        "thursday" : "Thursday",
        "friday"   : "Friday",
        "saturday" : "Saturday",
        "sunday"   : "Sunday",
        "തിങ്കൾ"   : "Monday",
        "ചൊവ്വ"    : "Tuesday",
        "ബുധൻ"     : "Wednesday",
        "വ്യാഴം"   : "Thursday",
        "വെള്ളി"   : "Friday",
        "Thinkal"   : "Monday",
        "chovva"  : "Tuesday",
        "budhan": "Wednesday",
        "vyazham" : "Thursday",
        "velli"   : "Friday",
        "shani" : "Saturday",
        "njayar"   : "Sunday"
    }

    for word, date in date_words.items():
        if word in text_lower:
            return date

    return None

# ── Time of Day Extraction ────────────────────────────────────
def extract_time(text: str) -> str | None:
    text_lower = text.lower()

    # Specific time (e.g. 10 am, 4:30)
    time_match = re.search(
        r'\b(\d{1,2})\s*(am|pm|maniku|mani|:00)\b',
        text_lower
    )
    if time_match:
        return time_match.group(0)

    # Time of day
    for period in ["morning", "ravile", "afternoon", "uchakku",
                   "evening", "vaikunneram", "night", "raatri"]:
        if period in text_lower:
            return period

    return None

# ── Keyword Backup Intent ─────────────────────────────────────
def keyword_backup(text: str) -> str | None:
    text_lower = text.lower()
    queue_phrases = [
    "ahead of me",
    "before me",
    "queue position",
    "my turn",
    "waiting before me",
    "people are ahead",
]

    for phrase in queue_phrases:
        if phrase in text_lower:
            return "token_status"
    # Priority phrases checked first — fixes ambiguous overlaps
    priority_phrases = {

    # ---------- Token Status ----------
    "booking confirmed": "token_status",
    "is my booking": "token_status",
    "token status": "token_status",
    "token number": "token_status",
    "check my token": "token_status",

    # ---------- Cancel ----------
    "cancel cheyyanam": "cancel_token",
    "cancel cheyyu": "cancel_token",
    "cancel my appointment": "cancel_token",
    "booking cancel": "cancel_token",
    "njan varaan patilla": "cancel_token",

    # ---------- OP ----------
    "op timing": "op_enquiry",
    "op schedule": "op_enquiry",
    "op open": "op_enquiry",
    "is op": "op_enquiry",
    "op available": "op_enquiry",

    # ---------- Booking ----------
    "book token": "token_booking",
    "book appointment": "token_booking",
    "appointment venam": "token_booking",
    "token venam": "token_booking",
    "doctor kanam": "token_booking",

    # ---------- Doctor Availability ----------
    "doctor available": "doctor_availability",
    "doctor today": "doctor_availability",
    "doctor tomorrow": "doctor_availability",
    "doctors today": "doctor_availability",
    "doctors tomorrow": "doctor_availability",
    "show me doctors": "doctor_availability",
    "list doctors": "doctor_availability",
    "any doctors": "doctor_availability",
}
    for phrase, intent in priority_phrases.items():
        if phrase in text_lower:
            return intent

    # Normal keyword scoring as fallback
    scores = {intent: 0 for intent in KEYWORD_RULES}
    for intent, keywords in KEYWORD_RULES.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[intent] += 1

    best_intent = max(scores, key=scores.get)
    if scores[best_intent] > 0:
        return best_intent
    return None

# ── Main Function (Person 4 calls this) ──────────────────────
# ── Main Function (Person 4 calls this) ──────────────────────
def extract_intent_slots(text: str) -> dict:

    if model is None or tokenizer is None:
        return {
            "intent"    : "unknown",
            "confidence": 0.0,
            "slots"     : {},
            "error"     : "Model not loaded. Call load_model() first."
        }

    # ── Step 1: Always run the model first (no more intent hijacking) ─
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        padding=True,
    )

    with torch.no_grad():
        outputs    = model(**inputs)
        probs      = torch.softmax(outputs.logits, dim=1)
        confidence = probs.max().item()
        pred_idx   = probs.argmax().item()

    predicted_intent = INTENT_LABELS[pred_idx]

    # ── Step 2: Extract all slots (including symptom-based department) ─
    slots = {
        "department"  : extract_department(text),
        "doctor"      : extract_doctor(text),
        "date"        : extract_date(text),
        "time"        : extract_time(text),
        "token_number": extract_token_number(text),
    }

    # Add symptom detection info
    if is_symptom_query(text):
        dept_from_symptom = symptom_triage(text)
        if dept_from_symptom and not slots.get("department"):
            slots["department"] = dept_from_symptom
        slots["has_symptom"] = True

    # Remove None values
    slots = {k: v for k, v in slots.items() if v is not None}

    # ── Step 3: Confidence-based intent resolution ─────────────────
    # ── Step 3: Intent Resolution ─────────────────────────────

    text_lower = text.lower()

    # High confidence → Always trust MuRIL
    if confidence >= 0.75:
        final_intent = predicted_intent

    # Medium confidence
    elif confidence >= 0.50:

        # OP queries should stay OP
        if "op" in text_lower:
            final_intent = "op_enquiry"

        # Department + doctor → doctor availability
        elif slots.get("department") and "doctor" in text_lower:
            final_intent = "doctor_availability"

        else:
            backup = keyword_backup(text)
            final_intent = backup if backup else predicted_intent

    # Low confidence
    else:

        backup = keyword_backup(text)

        if backup:
            final_intent = backup

        elif slots.get("has_symptom"):
            final_intent = "token_booking"
            confidence = 0.65

        elif slots.get("department"):
            final_intent = predicted_intent

        else:
            return {
                "intent": "unclear",
                "confidence": round(confidence, 4),
                "slots": {},
                "reply": "Sorry, could you please rephrase that?"
            }
        
    return{
        "intent"    : final_intent,
        "confidence": round(confidence, 4),
        "slots"     : slots,
    }