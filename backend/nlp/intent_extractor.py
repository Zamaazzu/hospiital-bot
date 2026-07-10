# backend/nlp/intent_extractor.py

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

# ── Words that signal doctor availability intent ───────────────
DOCTOR_AVAILABILITY_SIGNALS = [
    "doctor available", "doctors available",
    "doctor today", "doctors today",
    "doctor tomorrow", "doctors tomorrow",
    "doctor undo", "doctor und",
    "doctor innu", "doctor nale",
    "doctor free", "doctor duty",
    "doctor varmo", "doctor here",
    "show me doctors", "list doctors",
    "any doctors", "doctors in",
    "doctor in ", "is there a doctor",
    "is there an", "doctors available",
    "doctor available in", "doctor available tomorrow",
    "doctor available today",
]

# ── Words that signal token booking intent ────────────────────
BOOKING_SIGNALS = [
    "book a token", "book token", "book me a",
    "book a slot", "book me a slot",
    "book appointment", "make appointment",
    "need appointment", "need a token",
    "want appointment", "want a token",
    "get appointment", "get a token",
    "schedule appointment", "fix appointment",
    "appointment venam", "token venam",
    "slot venam", "book cheyyanam",
    "token book", "slot book",
    "reserve a token", "reserve token",
    "doctor kanam", "doctor kaanam",
    "kanaanam", "pettannu",
    "token vangan", "vangan varunnu",
]

# ── Words that signal token status intent ─────────────────────
STATUS_SIGNALS = [
    "ahead of me", "before me",
    "people ahead", "people are ahead",
    "how many people", "how many more",
    "how long more", "how long will",
    "queue position", "my turn",
    "waiting time", "waiting since",
    "token status", "check my token",
    "token number", "my token number",
    "check my number", "booking confirmed",
    "is my booking", "has my token",
    "token called", "token vilikumo",
    "evide ethi", "token evide",
    "ente turn", "eppo vilikum",
    "ethra per munnil",
]

# ── Words that signal cancel intent ──────────────────────────
CANCEL_SIGNALS = [
    "cancel cheyyanam", "cancel cheyyu",
    "cancel my appointment", "cancel my token",
    "cancel my booking", "booking cancel",
    "njan varaan patilla", "varaan patilla",
    "varan patilla", "pokaan patilla",
    "varaan kazhiyilla", "kazhiyilla",
    "budhimuttu", "venda ipo",
    "token venda", "appointment venda",
    "remove booking", "delete token",
    "withdraw token", "stop appointment",
    "i cant come", "cannot come",
    "won't make it", "not coming",
]

# ── Words that signal OP enquiry intent ──────────────────────
OP_SIGNALS = [
    "op timing", "op schedule",
    "op open", "op available",
    "op undo", "op und",
    "op innu", "op nale",
    "is op", "op hours",
    "op start", "op end",
    "enthu cheyyum", "op?",
    "what are your op", "hospital open",
    "outpatient", "when is op",
    "op running", "op closed",
]

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

# ── Check if text is meaningful ───────────────────────────────
def is_meaningful(text: str) -> bool:
    """
    Returns False for:
    - Empty or whitespace only
    - Pure gibberish (no real words, no Malayalam)
    - Too short (single char)
    - Keyboard-mash gibberish (long consonant runs, no real vowel pattern)
    """
    text = text.strip()
    if len(text) < 2:
        return False

    # Check if it has at least one real word (3+ chars)
    words = text.split()
    real_words = [w for w in words if len(w) >= 3]
    if not real_words:
        return False

    # Check if it looks like complete gibberish
    # (all consonants, no vowels, no Malayalam chars)
    has_vowel     = bool(re.search(r'[aeiouAEIOU]', text))
    has_malayalam = bool(re.search(r'[\u0D00-\u0D7F]', text))
    has_number    = bool(re.search(r'\d', text))

    if not has_vowel and not has_malayalam and not has_number:
        return False

    # Keyboard-mash check: real English/transliterated words rarely have
    # 4+ consecutive consonants. If every "real" word has a long consonant
    # run, treat the whole input as gibberish (e.g. "asdkfj alskdjf").
    # Skip this check for Malayalam script since it has its own structure.
    if not has_malayalam:
        consonant_run = re.compile(r'[^aeiouAEIOU\s\d]{4,}')
        if all(consonant_run.search(w) for w in real_words):
            return False

    return True

# ── Department Extraction ─────────────────────────────────────
def extract_department(text: str) -> str | None:
    text_lower = text.lower()

    # Skip very short text (avoids false positives on single words like "OP")
    if len(text.strip()) <= 3:
        return None

    # Step 1: Symptom → Department (highest priority)
    if is_symptom_query(text):
        dept = symptom_triage(text)
        if dept:
            return dept

    # Step 2: Gazetteer aliases (word-boundary match to avoid substring
    # false positives, e.g. "ent" inside "Gastroenterology")
    for alias, official in alias_map.items():
        if re.search(rf'\b{re.escape(alias)}\b', text_lower):
            return official

    # Step 3: Exact department name match (case insensitive, word boundary)
    for dept in DEPARTMENTS:
        if re.search(rf'\b{re.escape(dept.lower())}\b', text_lower):
            return dept

    # Step 4: Fuzzy match — only for longer texts to avoid false positives
    # Short texts like "cancel" shouldn't fuzzy-match to "Cancer Care"
    if len(text.split()) >= 2:
        match, score = process.extractOne(
            text,
            DEPARTMENTS,
            scorer=fuzz.token_sort_ratio  # more reliable than partial_ratio
        )
        if score >= 85:
            return match

    return None

# ── Doctor Name Extraction ────────────────────────────────────
def extract_doctor(text: str) -> str | None:
    # Only match when "Dr." or "Doctor" is explicitly present with capital name
    pattern = r'\b(?:Dr\.?|Doctor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
    match   = re.search(pattern, text)  # no IGNORECASE prevents garbage matches
    if match:
        name = match.group(1).strip()
        # Remove trailing time/date words accidentally captured
        stop_words = [
            "nale", "innu", "today", "tomorrow", "morning",
            "evening", "night", "ravile", "vaikunneram",
            "uchakku", "raatri", "available", "free", "duty"
        ]
        name_parts = [p for p in name.split() if p.lower() not in stop_words]
        return " ".join(name_parts) if name_parts else None
    return None

# ── Token Number Extraction ───────────────────────────────────
def extract_token_number(text: str) -> str | None:
    # Match formats: CAR-20260710-001 or plain numbers 1-9999
    # Avoid matching years (4-digit numbers starting with 19xx or 20xx)
    pattern = r'\b([A-Z]{2,4}-\d{6,8}-\d{2,4})\b'
    match   = re.search(pattern, text)
    if match:
        return match.group(1)

    # Plain short numbers (1-3 digits only, to avoid year false positives)
    plain = re.search(r'\b(\d{1,3})\b', text)
    if plain:
        return plain.group(1)

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
        "thinkal"  : "Monday",
        "chovva"   : "Tuesday",
        "budhan"   : "Wednesday",
        "vyazham"  : "Thursday",
        "velli"    : "Friday",
        "shani"    : "Saturday",
        "njayar"   : "Sunday",
        "തിങ്കൾ"   : "Monday",
        "ചൊവ്വ"    : "Tuesday",
        "ബുധൻ"     : "Wednesday",
        "വ്യാഴം"   : "Thursday",
        "വെള്ളി"   : "Friday",
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

    # Time of day keywords
    for period in ["morning", "ravile", "afternoon", "uchakku",
                   "evening", "vaikunneram", "night", "raatri"]:
        if period in text_lower:
            return period

    return None

# ── Signal-Based Intent Detection ────────────────────────────
def detect_intent_from_signals(text: str) -> str | None:
    """
    Checks ordered signal lists to detect intent.
    More reliable than keyword scoring for ambiguous cases.
    Signals are checked in order of specificity (most specific first).
    """
    text_lower = text.lower()

    # Check status signals first (most specific phrases)
    for signal in STATUS_SIGNALS:
        if signal in text_lower:
            return "token_status"

    # Check cancel signals
    for signal in CANCEL_SIGNALS:
        if signal in text_lower:
            return "cancel_token"

    # Check booking signals
    for signal in BOOKING_SIGNALS:
        if signal in text_lower:
            return "token_booking"

    # Check OP signals
    for signal in OP_SIGNALS:
        if signal in text_lower:
            return "op_enquiry"

    # Check doctor availability signals
    for signal in DOCTOR_AVAILABILITY_SIGNALS:
        if signal in text_lower:
            return "doctor_availability"

    return None

# ── Main Function (Person 4 calls this) ──────────────────────
def extract_intent_slots(text: str) -> dict:

    # ── Guard: empty or meaningless input ────────────────────
    if not text or not text.strip():
        return {
            "intent"    : "unclear",
            "confidence": 0.0,
            "slots"     : {},
            "reply"     : "Sorry, I didn't catch that. Could you please speak again?"
        }

    if not is_meaningful(text):
        return {
            "intent"    : "unclear",
            "confidence": 0.0,
            "slots"     : {},
            "reply"     : "Sorry, I couldn't understand. Could you please rephrase?"
        }

    if model is None or tokenizer is None:
        return {
            "intent"    : "unknown",
            "confidence": 0.0,
            "slots"     : {},
            "error"     : "Model not loaded. Call load_model() first."
        }

    # ── Step 1: Run MuRIL model ───────────────────────────────
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

    # ── Step 2: Extract all slots ─────────────────────────────
    slots = {
        "department"  : extract_department(text),
        "doctor"      : extract_doctor(text),
        "date"        : extract_date(text),
        "time"        : extract_time(text),
        "token_number": extract_token_number(text),
    }

    # Flag symptom queries and ensure department is set
    if is_symptom_query(text):
        dept_from_symptom = symptom_triage(text)
        if dept_from_symptom and not slots.get("department"):
            slots["department"] = dept_from_symptom
        slots["has_symptom"] = True

    # Remove None values — clean output for Person 4
    slots = {k: v for k, v in slots.items() if v is not None}

    # ── Step 3: Symptom override ──────────────────────────────
    # Pure symptom with no OP/doctor context → always token_booking
    if slots.get("has_symptom"):
        text_lower_check = text.lower()
        no_doctor_context = all(
            kw not in text_lower_check
            for kw in ["op", "doctor", "available", "duty", "free"]
        )
        if no_doctor_context:
            return {
                "intent"    : "token_booking",
                "confidence": round(confidence, 4),
                "slots"     : slots,
            }

    # ── Step 4: Intent resolution ─────────────────────────────
    text_lower = text.lower()

    # High confidence (≥0.75) → trust MuRIL completely
    if confidence >= 0.75:
        final_intent = predicted_intent

    # Medium confidence (0.50-0.75) → use signals + context
    elif confidence >= 0.50:

        # Try signal detection first (most reliable for ambiguous cases)
        signal_intent = detect_intent_from_signals(text)

        if signal_intent:
            final_intent = signal_intent

        # OP keyword in text → strongly suggests op_enquiry
        elif "op" in text_lower and "book" not in text_lower and "token" not in text_lower:
            final_intent = "op_enquiry"

        # Department + doctor keyword → doctor availability
        elif slots.get("department") and "doctor" in text_lower and "book" not in text_lower:
            final_intent = "doctor_availability"

        # Department + booking keyword → token booking
        elif slots.get("department") and any(
            kw in text_lower for kw in ["book", "token", "slot", "appointment", "venam"]
        ):
            final_intent = "token_booking"

        # Fall back to MuRIL prediction
        else:
            final_intent = predicted_intent

    # Low confidence (<0.50) → signals or fallback
    else:
        signal_intent = detect_intent_from_signals(text)

        if signal_intent:
            final_intent = signal_intent

        elif slots.get("has_symptom"):
            # Symptom present but low confidence → booking
            final_intent = "token_booking"

        elif slots.get("department") and "doctor" in text_lower:
            final_intent = "doctor_availability"

        elif slots.get("department"):
            # Department found but unclear action → op enquiry
            final_intent = "op_enquiry"

        else:
            # Truly unclear — ask user to repeat
            return {
                "intent"    : "unclear",
                "confidence": round(confidence, 4),
                "slots"     : {},
                "reply"     : "Sorry, could you please rephrase that?"
            }

    # ── Step 5: Return result ─────────────────────────────────
    return {
        "intent"    : final_intent,
        "confidence": round(confidence, 4),
        "slots"     : slots,
    }

# ── Load on startup ───────────────────────────────────────────
load_model()