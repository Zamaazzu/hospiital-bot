# data/merge_datasets.py

import json

files = [
    "intent_dataset_v2.json",   # 2248 samples
    "informal_samples.json",    # new targeted samples
]

merged = []
for file in files:
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
        merged.extend(data)
        print(f"{file}: {len(data)} samples")

print(f"\nTotal merged: {len(merged)} samples")

# Save as v3 — don't overwrite v2
with open("intent_dataset_v3.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("Saved as intent_dataset_v3.json")