from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("google/muril-base-cased")

model = AutoModelForSequenceClassification.from_pretrained(
    "google/muril-base-cased",
    num_labels=5
)

text = "I need an OP token"

inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

print(outputs.logits)
print(outputs.logits.shape)