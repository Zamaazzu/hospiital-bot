# backend/nlp/symptom_triage.py

SYMPTOM_MAP = {

    # ── Cardiology ────────────────────────────────────────
    "nenju vedana": "Cardiology",
    "nenju valivu": "Cardiology",
    "chest pain": "Cardiology",
    "heart pain": "Cardiology",
    "maarbu vedana": "Cardiology",
    "heartbeat": "Cardiology",
    "palpitation": "Cardiology",
    "nenju midichu": "Cardiology",
    "blood pressure": "Cardiology",
    "bp": "Cardiology",
    "heart": "Cardiology",
    "hridayam": "Cardiology",

    # ── Cardio Thoracic & Vascular Surgery ───────────────
    "vascular": "Cardio Thoracic & Vascular Surgery",
    "thoracic": "Cardio Thoracic & Vascular Surgery",
    "blood vessel": "Cardio Thoracic & Vascular Surgery",
    "varicose": "Cardio Thoracic & Vascular Surgery",

    # ── Neurology ─────────────────────────────────────────
    "thalavedhana": "Neurology",
    "thalaveda": "Neurology",
    "headache": "Neurology",
    "migraine": "Neurology",
    "thala valivu": "Neurology",
    "fits": "Neurology",
    "seizure": "Neurology",
    "stroke": "Neurology",
    "paralysis": "Neurology",
    "memory loss": "Neurology",
    "nerves": "Neurology",
    "thalach": "Neurology",

    # ── Neurosurgery ──────────────────────────────────────
    "brain surgery": "Neurosurgery",
    "spine surgery": "Neurosurgery",
    "spinal": "Neurosurgery",
    "brain tumor": "Neurosurgery",
    "mugacheri": "Neurosurgery",

    # ── Orthopaedics ──────────────────────────────────────
    "kalinu vedana": "Orthopaedics",
    "kalinu pottal": "Orthopaedics",
    "kali valivu": "Orthopaedics",
    "bone pain": "Orthopaedics",
    "joint pain": "Orthopaedics",
    "back pain": "Orthopaedics",
    "ellu valivu": "Orthopaedics",
    "fracture": "Orthopaedics",
    "broken bone": "Orthopaedics",
    "knee pain": "Orthopaedics",
    "moottu valivu": "Orthopaedics",
    "iduppu valivu": "Orthopaedics",
    "shoulder pain": "Orthopaedics",
    "elbow": "Orthopaedics",
    "arthritis": "Orthopaedics",
    "tol vedana":"Orthopaedics",

    # ── Dermatology ───────────────────────────────────────
    "mukha kuru": "Dermatology",
    "skin vedana": "Dermatology",
    "skin problem": "Dermatology",
    "skin rash": "Dermatology",
    "itching": "Dermatology",
    "choriyal": "Dermatology",
    "chorum": "Dermatology",
    "acne": "Dermatology",
    "eczema": "Dermatology",
    "psoriasis": "Dermatology",
    "kurukkal": "Dermatology",
    "hair fall": "Dermatology",
    "mudi pokal": "Dermatology",
    "mudi kozhichil": "Dermatology",

    # ── ENT ───────────────────────────────────────────────
    "chevi vedana": "ENT",
    "chevi": "ENT",
    "ear pain": "ENT",
    "hearing loss": "ENT",
    "kekkaan patunilla": "ENT",
    "nasal": "ENT",
    "nose block": "ENT",
    "mukkil": "ENT",
    "throat pain": "ENT",
    "thalayil valivu": "ENT",
    "tonsil": "ENT",
    "sinusitis": "ENT",
    "sneezing": "ENT",
    "tonsils": "ENT",
    "thummal": "ENT",

    # ── Gastroenterology ──────────────────────────────────
    "vayar valivu": "Gastroenterology",
    "vayar vedana": "Gastroenterology",
    "stomach pain": "Gastroenterology",
    "vayar": "Gastroenterology",
    "ulcer": "Gastroenterology",
    "acidity": "Gastroenterology",
    "vomiting": "Gastroenterology",
    "oakkam": "Gastroenterology",
    "diarrhea": "Gastroenterology",
    "constipation": "Gastroenterology",
    "liver": "Gastroenterology",
    "jaundice": "Gastroenterology",
    "manja pani": "Gastroenterology",
    "bloating": "Gastroenterology",

    # ── Paediatrics ───────────────────────────────────────
    "ente kunjinu pani": "Paediatrics",
    "kunjinu pani": "Paediatrics",
    "kutti pani": "Paediatrics",
    "kutti": "Paediatrics",
    "baby": "Paediatrics",
    "child fever": "Paediatrics",
    "children": "Paediatrics",
    "paediatric": "Paediatrics",
    "infant": "Paediatrics",
    "newborn": "Paediatrics",
    "kunjikku": "Paediatrics",
    "mon pani": "Paediatrics",
    "mol pani": "Paediatrics",

    # ── Neonatology ───────────────────────────────────────
    "newborn baby": "Neonatology",
    "premature baby": "Neonatology",
    "neonatal": "Neonatology",
    "puthu prani": "Neonatology",

    # ── Pulmanology ───────────────────────────────────────
    "chest congestion": "Pulmanology",
    "breathing problem": "Pulmanology",
    "shvaasam": "Pulmanology",
    "cough": "Pulmanology",
    "coughing": "Pulmanology",
    "cough blood": "Pulmanology",
    "asthma": "Pulmanology",
    "lungs": "Pulmanology",
    "shortness of breath": "Pulmanology",
    "tuberculosis": "Pulmanology",
    "tb": "Pulmanology",
    "chest tightness": "Pulmanology",

    # ── Nephrology ────────────────────────────────────────
    "kidney problem": "Nephrology",
    "kidney stone": "Nephrology",
    "kidney pain": "Nephrology",
    "mutramburappu": "Nephrology",
    "dialysis": "Nephrology",
    "urine problem": "Nephrology",
    "muthram": "Nephrology",
    "renal": "Nephrology",

    # ── Urology ───────────────────────────────────────────
    "urinary": "Urology",
    "bladder": "Urology",
    "prostate": "Urology",
    "muthram pokan kashtam": "Urology",
    "burning urination": "Urology",

    # ── Obstetrics & Gynaecology ──────────────────────────
    "pregnancy": "Obstetrics & Gynaecology",
    "pregnant": "Obstetrics & Gynaecology",
    "garbhini": "Obstetrics & Gynaecology",
    "periods": "Obstetrics & Gynaecology",
    "menstrual": "Obstetrics & Gynaecology",
    "masam": "Obstetrics & Gynaecology",
    "delivery": "Obstetrics & Gynaecology",
    "prasavam": "Obstetrics & Gynaecology",
    "gynecology": "Obstetrics & Gynaecology",
    "women problem": "Obstetrics & Gynaecology",
    "uterus": "Obstetrics & Gynaecology",

    # ── Infertility & Laparoscopy ─────────────────────────
    "infertility": "Infertility & Laparoscopy",
    "ivf": "Infertility & Laparoscopy",
    "unable to conceive": "Infertility & Laparoscopy",
    "no children": "Infertility & Laparoscopy",
    "laparoscopy": "Infertility & Laparoscopy",

    # ── Ophthalmology → closest is ENT but no eye dept ───
    # Map to Emergency Medicine as fallback
    "eye pain": "Emergency Medicine",
    "kannu vedana": "Emergency Medicine",
    "kannu": "Emergency Medicine",
    "vision problem": "Emergency Medicine",
    "kaan kazhikilla": "Emergency Medicine",

    # ── Dental Maxillofacial Surgery ──────────────────────
    "phal vedana": "Dental Maxillofacial Surgery",
    "tooth pain": "Dental Maxillofacial Surgery",
    "toothache": "Dental Maxillofacial Surgery",
    "phal": "Dental Maxillofacial Surgery",
    "gums": "Dental Maxillofacial Surgery",
    "jaw pain": "Dental Maxillofacial Surgery",
    "dental": "Dental Maxillofacial Surgery",

    # ── Cancer Care ───────────────────────────────────────
    "cancer": "Cancer Care",
    "tumor": "Cancer Care",
    "chemotherapy": "Cancer Care",
    "radiation": "Cancer Care",
    "arbuda rogam": "Cancer Care",

    # ── Physiotherapy ─────────────────────────────────────
    "physiotherapy": "Physiotherapy",
    "rehabilitation": "Physiotherapy",
    "exercise therapy": "Physiotherapy",
    "muscle pain": "Physiotherapy",
    "pesi valivu": "Physiotherapy",
    "stroke recovery": "Physiotherapy",
    "post surgery recovery": "Physiotherapy",

    # ── Emergency Medicine ────────────────────────────────
    "emergency": "Emergency Medicine",
    "accident": "Emergency Medicine",
    "unconscious": "Emergency Medicine",
    "bleeding": "Emergency Medicine",
    "raktha sraavam": "Emergency Medicine",
    "urgent": "Emergency Medicine",
    "vegam": "Emergency Medicine",

    # ── Child Development Centre ──────────────────────────
    "autism": "Child Development Centre",
    "speech delay": "Child Development Centre",
    "development delay": "Child Development Centre",
    "learning disability": "Child Development Centre",
    "adhd": "Child Development Centre",

    # ── Anaesthesiology ───────────────────────────────────
    "anaesthesia": "Anaesthesiology",
    "anesthesia": "Anaesthesiology",
    "pain management": "Anaesthesiology",

    # ── Interventional Radiology ──────────────────────────
    "angioplasty": "Interventional Radiology",
    "stent": "Interventional Radiology",
    "biopsy": "Interventional Radiology",

    # ── General fallback ──────────────────────────────────
    "fever": "Emergency Medicine",
    "pani": "Emergency Medicine",
    "pani pidicchu": "Emergency Medicine",
    "pani undu": "Emergency Medicine",
    "general": "Emergency Medicine",
    "not feeling well": "Emergency Medicine",
    "sukham illa": "Emergency Medicine",
    "arogya illayma": "Emergency Medicine",

    # ── Critical Care ─────────────────────────────────────────
"icu": "Critical Care",
"intensive care": "Critical Care",
"critical": "Critical Care",
"life support": "Critical Care",
"ventilator": "Critical Care",
"coma": "Critical Care",
"serious condition": "Critical Care",
"kodiya avasta": "Critical Care",
"avasta gauram": "Critical Care",
}


def symptom_triage(text: str) -> str:
    text_lower = text.lower()

    # Check multi-word phrases first (longer matches take priority)
    sorted_symptoms = sorted(SYMPTOM_MAP.keys(), key=len, reverse=True)

    for symptom in sorted_symptoms:
        if symptom in text_lower:
            return SYMPTOM_MAP[symptom]

    return "Emergency Medicine"  # default fallback