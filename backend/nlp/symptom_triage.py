# backend/nlp/symptom_triage.py

SYMPTOM_MAP = {

    #────Malayalam Added────────────────────────────────────
    "നെഞ്ചുവേദന": "Cardiology",
    "ഹൃദ്രോഗം": "Cardiology",
    "തലവേദന": "Neurology",
    "വയർ വേദന": "Gastroenterology",
    "ചെവി വേദന": "ENT",
    "ചുമ": "Pulmanology",
    "പനി": "Emergency Medicine",
    "കുട്ടിക്ക് പനി": "Paediatrics",
    "ഗർഭിണി": "Obstetrics & Gynaecology",
    "പല്ലുവേദന": "Dental Maxillofacial Surgery",
    "കാൽ വേദന": "Orthopaedics",
    "ശ്വാസതടസ്സം": "Pulmanology",
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
    "ഹൃദയം": "Cardiology",
    "ഹൃദയ": "Cardiology",
    "ഹൃദയവേദന": "Cardiology",
    "ഹൃദയത്തിന് വേദന": "Cardiology",
    "ഹൃദയത്തിൽ വേദന": "Cardiology",
    "ഹൃദയമിടിപ്പ്": "Cardiology",
    "ഹൃദയമിടിപ്പ് കൂടുന്നു": "Cardiology",
    "ഹൃദയമിടിപ്പ് കുറയുന്നു": "Cardiology",
    "ഹൃദയമിടിപ്പ് ക്രമമല്ല": "Cardiology",

    "നെഞ്ചുവേദന": "Cardiology",
    "നെഞ്ച് വേദന": "Cardiology",
    "നെഞ്ചിന് വേദന": "Cardiology",
    "നെഞ്ചിൽ വേദന": "Cardiology",
    "നെഞ്ചിടിപ്പ്": "Cardiology",

    "ഹൃദ്രോഗം": "Cardiology",
    "ഹാർട്ട്": "Cardiology",
    "ഹാർട്ട് പ്രശ്നം": "Cardiology",
    "ഹാർട്ട് അറ്റാക്ക്": "Cardiology",

    "രക്തസമ്മർദ്ദം": "Cardiology",
    "ഉയർന്ന രക്തസമ്മർദ്ദം": "Cardiology",
    "കുറഞ്ഞ രക്തസമ്മർദ്ദം": "Cardiology",
    "ബ്ലഡ് പ്രഷർ": "Cardiology",
    "ബി.പി": "Cardiology",

    # ── Cardio Thoracic & Vascular Surgery ───────────────
    "vascular": "Cardio Thoracic & Vascular Surgery",
    "thoracic": "Cardio Thoracic & Vascular Surgery",
    "blood vessel": "Cardio Thoracic & Vascular Surgery",
    "varicose": "Cardio Thoracic & Vascular Surgery",

    "ബൈപാസ്": "Cardio Thoracic & Vascular Surgery",
    "ബൈപാസ് സർജറി": "Cardio Thoracic & Vascular Surgery",
    "ഹൃദയ ശസ്ത്രക്രിയ": "Cardio Thoracic & Vascular Surgery",
    "ഹാർട്ട് സർജറി": "Cardio Thoracic & Vascular Surgery",
    "ഓപ്പൺ ഹാർട്ട് സർജറി": "Cardio Thoracic & Vascular Surgery",

    "രക്തക്കുഴൽ": "Cardio Thoracic & Vascular Surgery",
    "രക്തക്കുഴലിലെ തടസം": "Cardio Thoracic & Vascular Surgery",
    "രക്തക്കുഴൽ അടഞ്ഞു": "Cardio Thoracic & Vascular Surgery",
    "രക്തക്കുഴൽ ബ്ലോക്ക്": "Cardio Thoracic & Vascular Surgery",

    "വെരിക്കോസ്": "Cardio Thoracic & Vascular Surgery",
    "വെരിക്കോസ് വെയിൻ": "Cardio Thoracic & Vascular Surgery",
    "വെരിക്കോസ് വെയിൻസ്": "Cardio Thoracic & Vascular Surgery",
    "ഞരമ്പ് വീക്കം": "Cardio Thoracic & Vascular Surgery",
    "കാലിലെ ഞരമ്പ് വീക്കം": "Cardio Thoracic & Vascular Surgery",
    "ഞരമ്പ് തടിച്ചു": "Cardio Thoracic & Vascular Surgery",

    "നെഞ്ച് ശസ്ത്രക്രിയ": "Cardio Thoracic & Vascular Surgery",
    "ശ്വാസകോശ ശസ്ത്രക്രിയ": "Cardio Thoracic & Vascular Surgery",

    "അന്യൂറിസം": "Cardio Thoracic & Vascular Surgery",
    "അയോർട്ട": "Cardio Thoracic & Vascular Surgery",
    "അയോർട്ടിക്": "Cardio Thoracic & Vascular Surgery",

    # ── Neurology ─────────────────────────────────────────
    "headache": "Neurology",
    "migraine": "Neurology",
    "thala valivu": "Neurology",
    "fits": "Neurology",
    "seizure": "Neurology",
    "stroke": "Neurology",
    "paralysis": "Neurology",
    "memory loss": "Neurology",
    "nerves": "Neurology",

# Headache
"തലവേദന": "Neurology",
"തല വേദന": "Neurology",
"തലവേദനയുണ്ട്": "Neurology",
"കടുത്ത തലവേദന": "Neurology",
"തല പൊട്ടുന്ന പോലെ വേദന": "Neurology",
"മൈഗ്രെയ്ൻ": "Neurology",
"ഒറ്റത്തലവേദന": "Neurology",

# Dizziness
"തലകറക്കം": "Neurology",
"തല ചുറ്റൽ": "Neurology",
"തല ചുറ്റുന്നു": "Neurology",
"കറക്കം": "Neurology",
"ബാലൻസ് കിട്ടുന്നില്ല": "Neurology",

# Numbness
"മരവിപ്പ്": "Neurology",
"കൈ മരവിപ്പ്": "Neurology",
"കാല് മരവിപ്പ്": "Neurology",
"വിരൽ മരവിപ്പ്": "Neurology",
"മുഖം മരവിപ്പ്": "Neurology",

# Weakness
"കൈക്ക് ബലം ഇല്ല": "Neurology",
"കാലിന് ബലം ഇല്ല": "Neurology",
"ഒരു വശം ബലം ഇല്ല": "Neurology",
"ശരീരം തളരുന്നു": "Neurology",

# Stroke
"പക്ഷാഘാതം": "Neurology",
"സ്ട്രോക്ക്": "Neurology",
"സ്ട്രോക്ക് വന്നിട്ടുണ്ട്": "Neurology",
"വായ് കോടൽ": "Neurology",
"വായ് ഒരു വശത്തേക്ക് പോകുന്നു": "Neurology",

# Seizure
"അപസ്മാരം": "Neurology",
"ഫിറ്റ്സ്": "Neurology",
"വലിവ്": "Neurology",
"വലിവ് വരുന്നു": "Neurology",
"ബോധം പോകുന്നു": "Neurology",

# Memory
"ഓർമ്മക്കുറവ്": "Neurology",
"കാര്യങ്ങൾ മറക്കുന്നു": "Neurology",
"ഓർമ്മ പോകുന്നു": "Neurology",

# Tremor
"കൈ വിറയ്ക്കുന്നു": "Neurology",
"വിറയൽ": "Neurology",
"ശരീരം വിറയ്ക്കുന്നു": "Neurology",

"സംസാരിക്കാൻ പറ്റുന്നില്ല": "Neurology",
"സംസാരം വ്യക്തമല്ല": "Neurology",

"ഞരമ്പ്": "Neurology",
"ഞരമ്പ് രോഗം": "Neurology",
"ഞരമ്പ് പ്രശ്നം": "Neurology",

    # ── Neurosurgery ──────────────────────────────────────
    "brain surgery": "Neurosurgery",
    "spine surgery": "Neurosurgery",
    "spinal": "Neurosurgery",
    "brain tumor": "Neurosurgery",
    "mugacheri": "Neurosurgery",
    # ── Neurosurgery (Malayalam) ─────────────────────────

    "ന്യൂറോസർജറി": "Neurosurgery",
    "തലക്ക് ഗുരുതര പരിക്ക്": "Neurosurgery",
    "തലച്ചോറിൽ ട്യൂമർ": "Neurosurgery",
    "ബ്രെയിൻ ട്യൂമർ": "Neurosurgery",
    "നട്ടെല്ലിന് പരിക്ക്": "Neurosurgery",
    "നട്ടെല്ല് പ്രശ്നം": "Neurosurgery",
    "നട്ടെല്ല് ശസ്ത്രക്രിയ": "Neurosurgery",
    "ഡിസ്ക് സ്ലിപ്പ്": "Neurosurgery",
    "സ്ലിപ്പ് ഡിസ്ക്": "Neurosurgery",
    "സ്പൈൻ പ്രശ്നം": "Neurosurgery",
    "സ്പൈൻ സർജറി": "Neurosurgery",

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
    "knee hurts": "Orthopaedics",
    "moottu valivu": "Orthopaedics",
    "iduppu valivu": "Orthopaedics",
    "shoulder pain": "Orthopaedics",
    "elbow": "Orthopaedics",
    "arthritis": "Orthopaedics",
    "tol vedana":"Orthopaedics",
    "deham vedana":"Orthopaedics",
    "vedana":"Orthopaedics",
    # ── Orthopaedics (Malayalam) ─────────────────────────


    # Bone
    "എല്ല്": "Orthopaedics",
    "എല്ലുവേദന": "Orthopaedics",
    "എല്ല് ഒടിഞ്ഞു": "Orthopaedics",
    "ഒടിവ്": "Orthopaedics",

    # Joint
    "സന്ധിവേദന": "Orthopaedics",
    "സന്ധിക്ക് വേദന": "Orthopaedics",
    "സന്ധി വീക്കം": "Orthopaedics",
    "ദേഹം വേദന ":"Orthopaedics",

    # Knee
    "മുട്ടുവേദന": "Orthopaedics",
    "മുട്ടിന് വേദന": "Orthopaedics",
    "മുട്ട് വീക്കം": "Orthopaedics",

    # Leg / Hand
    "കാൽവേദന": "Orthopaedics",
    "കൈവേദന": "Orthopaedics",

    # Back / Neck
    "നടുവേദന": "Orthopaedics",
    "പുറംവേദന": "Orthopaedics",
    "കഴുത്തുവേദന": "Orthopaedics",
    "തോൾ വേദന ":"Orthopaedics",

    # Shoulder
    "തോളുവേദന": "Orthopaedics",
    "തോളിന് വേദന": "Orthopaedics",

    # Common
    "ഉളുക്ക്": "Orthopaedics",
    "പേശിവേദന": "Orthopaedics",
    "ആർത്രൈറ്റിസ്": "Orthopaedics",


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
    "mukhath paad": "Dermatology",
    "paad": "Dermatology",
    # ── Dermatology (Malayalam) ─────────────────────────
    "ത്വക്ക്": "Dermatology",
    "തൊലി": "Dermatology",
    "ത്വക്ക് രോഗം": "Dermatology",
    "ചർമ്മരോഗം": "Dermatology",

    # Itching
    "ചൊറിച്ചിൽ": "Dermatology",
    "ചൊറിച്ചിലുണ്ട്": "Dermatology",
    "തൊലിയിൽ ചൊറിച്ചിൽ": "Dermatology",
    "തൊലി ചൊറിയുന്നു": "Dermatology",

    # Rashes / Allergy
    "തിണർപ്പ്": "Dermatology",
    "തൊലിയിൽ തിണർപ്പ്": "Dermatology",
    "അലർജി": "Dermatology",
    "തൊലി അലർജി": "Dermatology",
    "തെണുത്തു":"Dermatology",

    # Pimples
    "മുഖക്കുരു": "Dermatology",
    "കുരു": "Dermatology",

    # Skin spots
    "പാടുകൾ": "Dermatology",
    "കറുത്ത പാടുകൾ": "Dermatology",
    "വെള്ള പാടുകൾ": "Dermatology",

    # Hair
    "മുടികൊഴിച്ചിൽ": "Dermatology",
    "മുടി കൊഴിയുന്നു": "Dermatology",

    # Infection
    "പൂപ്പൽ": "Dermatology",
    "കുരുക്കൾ": "Dermatology",
    "തൊലി പൊട്ടുന്നു": "Dermatology",

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
    # ── ENT (Malayalam) ───────────────────────────────────
"ചെവി": "ENT",
"മൂക്ക്": "ENT",
"തൊണ്ട": "ENT",

# Ear
"ചെവി വേദന": "ENT",
"ചെവിവേദന": "ENT",
"ചെവിയിൽ വേദന": "ENT",
"ചെവിയിൽ ശബ്ദം": "ENT",
"കേൾവിക്കുറവ്": "ENT",
"കേൾക്കാൻ ബുദ്ധിമുട്ട്": "ENT",

# Nose
"മൂക്ക് ":"ENT",
"മൂക്കടപ്പ്": "ENT",
"മൂക്കിൽ നിന്ന് രക്തം": "ENT",
"മൂക്കൊലിപ്പ്": "ENT",
"മൂക്കിൽ വെള്ളം വരുന്നു": "ENT",
"സൈനസൈറ്റിസ്": "ENT",
"സൈനസ്": "ENT",

# Throat
"തൊണ്ടവേദന": "ENT",
"തൊണ്ട വേദന": "ENT",
"തൊണ്ടയിൽ വേദന": "ENT",
"തൊണ്ടവീക്കം": "ENT",
"തൊണ്ടയിൽ അണുബാധ": "ENT",
"ടോൺസിൽ": "ENT",
"ടോൺസിലൈറ്റിസ്": "ENT",
"ശബ്ദം പോകുന്നു": "ENT",
"ശബ്ദം ഇരിക്കുന്നു": "ENT",

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
    # ── Gastroenterology (Malayalam) ─────────────────────────
# Stomach pain
"വയർ": "Gastroenterology",
"വയറുവേദന": "Gastroenterology",
"വയറിന് വേദന": "Gastroenterology",
"വയറിൽ വേദന": "Gastroenterology",
"വയറുവേദനയുണ്ട്": "Gastroenterology",

# Digestion
"ദഹനക്കേട്": "Gastroenterology",
"ഗ്യാസ്": "Gastroenterology",
"അസിഡിറ്റി": "Gastroenterology",
"നെഞ്ചെരിച്ചിൽ": "Gastroenterology",

# Vomiting / Diarrhoea
"ഛർദ്ദി": "Gastroenterology",
"ഛർദ്ദിക്കുന്നു": "Gastroenterology",
"വയറിളക്കം": "Gastroenterology",
"മലബന്ധം": "Gastroenterology",
"ശർദിൽ ":"Gastroenterology",
"ശർദിക്കുന്നു ":"Gastroenterology",

# Liver
"കരൾ": "Gastroenterology",
"കരൾ രോഗം": "Gastroenterology",
"മഞ്ഞപ്പിത്തം": "Gastroenterology",

# Others
"അൾസർ": "Gastroenterology",
"വയറിൽ കത്തൽ": "Gastroenterology",
"വയറിൽ അസ്വസ്ഥത": "Gastroenterology",
"വയര് ഉരുണ്ട്":"Gastroenterology",
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
    "monu pani": "Paediatrics",
    "molku pani": "Paediatrics",
    "makkalku pani": "Paediatrics",
    # ── Paediatrics (Malayalam) ────────────────────────
"ശിശുരോഗം": "Paediatrics",

# Child
"കുട്ടി": "Paediatrics",
"കുഞ്ഞ്": "Paediatrics",
"കുഞ്ഞിന്": "Paediatrics",
"കുട്ടിക്ക്": "Paediatrics",
"മോൻ": "Paediatrics",
"മകൾ": "Paediatrics",
"മക്കൾക്ക്":"Paediatrics",

# Common complaints
"കുട്ടിക്ക് പനി": "Paediatrics",
"കുഞ്ഞിന് പനി": "Paediatrics",
"കുട്ടിക്ക് ചുമ": "Paediatrics",
"കുഞ്ഞിന് ചുമ": "Paediatrics",
"കുട്ടിക്ക് ജലദോഷം": "Paediatrics",
"കുഞ്ഞിന് ജലദോഷം": "Paediatrics",
"കുട്ടിക്ക് വയറിളക്കം": "Paediatrics",
"കുഞ്ഞിന് വയറിളക്കം": "Paediatrics",
"കുട്ടിക്ക് ഛർദ്ദി": "Paediatrics",
"കുഞ്ഞിന് ഛർദ്ദി": "Paediatrics",

# General
"കുട്ടികളുടെ ഡോക്ടർ": "Paediatrics",
"ശിശുരോഗ വിദഗ്ധൻ": "Paediatrics",
    

    # ── Neonatology ───────────────────────────────────────
    "newborn baby": "Neonatology",
    "premature baby": "Neonatology",
    "neonatal": "Neonatology",
    "puthu prani": "Neonatology",
    # ── Neonatology (Malayalam) ─────────────────────────



"നവജാത ശിശു": "Neonatology",
"നവജാത കുഞ്ഞ്": "Neonatology",
"പിറന്ന കുഞ്ഞ്": "Neonatology",
"ജനിച്ച കുഞ്ഞ്": "Neonatology",
"പുതിയ കുഞ്ഞ്": "Neonatology",

"അകാല പ്രസവം": "Neonatology",
"കുറഞ്ഞ ഭാരം കുഞ്ഞ്": "Neonatology",
"ഇൻക്യുബേറ്റർ": "Neonatology",

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
    # ── Pulmonology (Malayalam) ─────────────────────────

"ശ്വാസകോശം": "Pulmanology",

# Breathing
"ശ്വാസതടസ്സം": "Pulmanology",
"ശ്വാസംമുട്ടൽ": "Pulmanology",
"ശ്വാസം കിട്ടുന്നില്ല": "Pulmanology",
"ശ്വാസം എടുക്കാൻ ബുദ്ധിമുട്ട്": "Pulmanology",
"ശ്വാസം വിടാൻ ബുദ്ധിമുട്ട്": "Pulmanology",

# Cough
"ചുമ": "Pulmanology",
"ചുമയുണ്ട്": "Pulmanology",
"വിട്ടുമാറാത്ത ചുമ": "Pulmanology",
"കഫം": "Pulmanology",
"കഫച്ചുമ": "Pulmanology",
"രക്തം ചുമക്കുന്നു": "Pulmanology",

# Diseases
"ആസ്ത്മ": "Pulmanology",
"ശ്വാസകോശ രോഗം": "Pulmanology",
"ന്യൂമോണിയ": "Pulmanology",
"ക്ഷയം": "Pulmanology",
"ടിബി": "Pulmanology",
"ബ്രോങ്കൈറ്റിസ്": "Pulmanology",
"ശ്വാസതടസ്സം": "Pulmanology",
"ശ്വാസതടസ്സമുണ്ട്": "Pulmanology",

# Others
"ശ്വാസകോശ അണുബാധ": "Pulmanology",
"വീസിംഗ്": "Pulmanology",

    # ── Nephrology ────────────────────────────────────────
    "kidney problem": "Nephrology",
    "kidney stone": "Nephrology",
    "kidney pain": "Nephrology",
    "mutramburappu": "Nephrology",
    "dialysis": "Nephrology",
    "urine problem": "Nephrology",
    "muthram": "Nephrology",
    "renal": "Nephrology",
    # ── Nephrology (Malayalam) ──────────────────────────

"വൃക്ക": "Nephrology",
"വൃക്കവേദന": "Nephrology",
"വൃക്കയ്ക്ക് വേദന": "Nephrology",
"വൃക്കരോഗം": "Nephrology",
"ഡയാലിസിസ്": "Nephrology",
"ക്രിയാറ്റിനിൻ": "Nephrology",
"വൃക്ക തകരാർ": "Nephrology",

    # ── Urology ───────────────────────────────────────────
    "urinary": "Urology",
    "bladder": "Urology",
    "prostate": "Urology",
    "muthram pokan kashtam": "Urology",
    "burning urination": "Urology",
    # ── Urology (Malayalam) ─────────────────────────────

"മൂത്രം": "Urology",
"മൂത്ര തടസ്സം": "Urology",
"മൂത്രം പോകുന്നില്ല": "Urology",
"മൂത്രത്തിൽ രക്തം": "Urology",
"മൂത്രത്തിന് കത്തൽ": "Urology",
"മൂത്രമൊഴിക്കാൻ ബുദ്ധിമുട്ട്": "Urology",
"കിഡ്നി സ്റ്റോൺ": "Urology",
"മൂത്രാശയം": "Urology",

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
    # ── Obstetrics & Gynaecology (Malayalam) ───────────

"ഗർഭം": "Obstetrics & Gynaecology",
"ഗർഭിണി": "Obstetrics & Gynaecology",
"ഗർഭ പരിശോധന": "Obstetrics & Gynaecology",
"പ്രസവം": "Obstetrics & Gynaecology",
"സ്ത്രീരോഗം": "Obstetrics & Gynaecology",
"മാസവരി": "Obstetrics & Gynaecology",
"ആർത്തവം": "Obstetrics & Gynaecology",

    # ── Infertility & Laparoscopy ─────────────────────────
    "infertility": "Infertility & Laparoscopy",
    "ivf": "Infertility & Laparoscopy",
    "unable to conceive": "Infertility & Laparoscopy",
    "no children": "Infertility & Laparoscopy",
    "laparoscopy": "Infertility & Laparoscopy",
    # ── Infertility & Laparoscopy (Malayalam) ──────────

"വന്ധ്യത": "Infertility & Laparoscopy",
"കുഞ്ഞ് ഇല്ല": "Infertility & Laparoscopy",
"ഗർഭം ധരിക്കുന്നില്ല": "Infertility & Laparoscopy",
"ഐവിഎഫ്": "Infertility & Laparoscopy",

    # ── Emergency Medicine (Malayalam) ──────────────────

"അത്യാഹിതം": "Emergency Medicine",
"അടിയന്തരം": "Emergency Medicine",
"അപകടം": "Emergency Medicine",
"രക്തസ്രാവം": "Emergency Medicine",
"ബോധം നഷ്ടപ്പെട്ടു": "Emergency Medicine",
"പൊള്ളൽ": "Emergency Medicine",
"വിഷം കഴിച്ചു": "Emergency Medicine",
"പാമ്പുകടി": "Emergency Medicine",
"നായ കടിച്ചു": "Emergency Medicine",
    "കണ്ണ് വേദന ": "Emergency Medicine",
    "കണ്ണ് ": "Emergency Medicine",
    "കാഴ്ച കുറവ് ": "Emergency Medicine",
    "കണ്ണ് കാണുന്നില്ല ": "Emergency Medicine",
    "കണ്ണിന്നു വേദനയുണ്ട്  ": "Emergency Medicine",

    # ── Dental Maxillofacial Surgery ──────────────────────
    "phal vedana": "Dental Maxillofacial Surgery",
    "tooth pain": "Dental Maxillofacial Surgery",
    "toothache": "Dental Maxillofacial Surgery",
    "phal": "Dental Maxillofacial Surgery",
    "gums": "Dental Maxillofacial Surgery",
    "jaw pain": "Dental Maxillofacial Surgery",
    "dental": "Dental Maxillofacial Surgery",
    # ── Dental Maxillofacial Surgery (Malayalam) ───────

"പല്ല്": "Dental Maxillofacial Surgery",
"പല്ലുവേദന": "Dental Maxillofacial Surgery",
"പല്ലിന് വേദന": "Dental Maxillofacial Surgery",
"പല്ല് ഒടിഞ്ഞു": "Dental Maxillofacial Surgery",
"മോണ": "Dental Maxillofacial Surgery",
"മോണയിൽ വേദന": "Dental Maxillofacial Surgery",
"താടി വേദന": "Dental Maxillofacial Surgery",
"വായിൽ മുറിവ്": "Dental Maxillofacial Surgery",

    # ── Cancer Care ───────────────────────────────────────
    "cancer": "Cancer Care",
    "tumor": "Cancer Care",
    "chemotherapy": "Cancer Care",
    "radiation": "Cancer Care",
    "arbuda rogam": "Cancer Care",
    # ── Cancer Care (Malayalam) ─────────────────────────

"കാൻസർ": "Cancer Care",
"അർബുദം": "Cancer Care",
"ട്യൂമർ": "Cancer Care",
"കീമോ": "Cancer Care",
"കീമോതെറാപ്പി": "Cancer Care",
"റേഡിയേഷൻ": "Cancer Care",
"ഓങ്കോളജി": "Cancer Care",

    # ── Physiotherapy ─────────────────────────────────────
    "physiotherapy": "Physiotherapy",
    "rehabilitation": "Physiotherapy",
    "exercise therapy": "Physiotherapy",
    "muscle pain": "Physiotherapy",
    "pesi valivu": "Physiotherapy",
    "stroke recovery": "Physiotherapy",
    "post surgery recovery": "Physiotherapy",
    # ── Physiotherapy (Malayalam) ───────────────────────

"വ്യായാമ ചികിത്സ": "Physiotherapy",
"പുനരധിവാസം": "Physiotherapy",
"കൈ വ്യായാമം": "Physiotherapy",
"കാൽ വ്യായാമം": "Physiotherapy",

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
    # ── Child Development Centre (Malayalam) ───────────

"ഓട്ടിസം": "Child Development Centre",
"ഓട്ടിസ്റ്റിക്": "Child Development Centre",
"എ.ഡി.എച്ച്.ഡി": "Child Development Centre",
"എഡിഎച്ച്ഡി": "Child Development Centre",
"സംസാരിക്കാൻ വൈകുന്നു": "Child Development Centre",
"സംസാരിക്കുന്നില്ല": "Child Development Centre",
"വികസന വൈകല്യം": "Child Development Centre",
"പഠന ബുദ്ധിമുട്ട്": "Child Development Centre",

    # ── Anaesthesiology ───────────────────────────────────
    "anaesthesia": "Anaesthesiology",
    "anesthesia": "Anaesthesiology",
    "pain management": "Anaesthesiology",
    # ── Anaesthesiology (Malayalam) ─────────────────────

"അനസ്തേഷ്യ": "Anaesthesiology",
"അനസ്തേഷ്യ നൽകണം": "Anaesthesiology",
"മയക്കുമരുന്ന്": "Anaesthesiology",
"ഓപ്പറേഷന് മുമ്പ്": "Anaesthesiology",
"ശസ്ത്രക്രിയയ്ക്ക് മുമ്പ്": "Anaesthesiology",

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
# ── Critical Care (Malayalam) ───────────────────────

"ഐസിയു": "Critical Care",
"ഐ.സി.യു": "Critical Care",
"ഇന്റൻസീവ് കെയർ": "Critical Care",
"വെന്റിലേറ്റർ": "Critical Care",
"അത്യാഹിത പരിചരണം": "Critical Care",
}

def normalize_symptom_text(text: str) -> str:
    """
    Normalize common Malayalam endings so that
    'വയറുവേദനയുണ്ട്' and 'വയറുവേദന'
    become the same for matching.
    """

    text = text.lower().strip()

    suffixes = [
        "യുണ്ട്",
        "ഉണ്ട്",
        "ആണ്",
        "യാണ്",
        "ആയിരുന്നു",
        "ആയിട്ടുണ്ട്",
    ]

    for suffix in suffixes:
        if text.endswith(suffix):
            text = text[:-len(suffix)].strip()

    return text

def symptom_triage(text: str) -> str:
    text = normalize_symptom_text(text)

    # Check multi-word phrases first (longer matches take priority)
    sorted_symptoms = sorted(SYMPTOM_MAP.keys(), key=len, reverse=True)

    for symptom in sorted_symptoms:
        if symptom in text:
            return SYMPTOM_MAP[symptom]

    return "Emergency Medicine"  # default fallback
sorted_symptoms = sorted(SYMPTOM_MAP.keys(), key=len, reverse=True)
def is_symptom_query(text: str) -> bool:
    """Check if text contains any symptom phrase"""
    text_lower = text.lower()
    for symptom in sorted_symptoms:
        if symptom in text_lower:
            return True
    return False