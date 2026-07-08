# backend/nlp/test_novel.py

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.nlp.intent_extractor import extract_intent_slots, load_model

load_model()

novel_queries = [
    "can you help me see a doctor please",
    "njan token vangan varunnu",
    "is there a wait",
    "my appointment got messed up",
    "eniku doctor kanaanam pettannu",
    "how long more",
    "I think I need to cancel this",
    "entha doctor ivide illathe",
    "waiting since long time",
    "can someone check my number",
]

print("=" * 60)
print("NOVEL QUERY TEST (not from training/test data)")
print("=" * 60)

for q in novel_queries:
    result = extract_intent_slots(q)
    print(f"\nQuery:      {q}")
    print(f"Intent:     {result['intent']}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    print(f"Slots:      {result.get('slots', {})}")