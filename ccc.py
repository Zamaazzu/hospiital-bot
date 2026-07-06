from collections import Counter
import json

with open("data/intent_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

counts = Counter(item["intent"] for item in data)

for intent, count in counts.items():
    print(f"{intent}: {count}")