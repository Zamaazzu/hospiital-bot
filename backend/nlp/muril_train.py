from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np
import json
import os
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ── Intents ──────────────────────────────────────────────
INTENTS = [
    "op_enquiry",
    "doctor_availability",
    "token_booking",
    "token_status",
    "cancel_token"
]

label2id = {intent: i for i, intent in enumerate(INTENTS)}
id2label  = {i: intent for i, intent in enumerate(INTENTS)}

MODEL_NAME = "google/muril-base-cased"
MODEL_SAVE = "../../models/intent_classifier"

# ── Load Dataset ─────────────────────────────────────────
def load_data(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    texts, labels = [], []
    skipped = 0

    for item in data:
        intent = item.get("intent", "").strip()
        text   = item.get("text",   "").strip()

        if intent not in label2id:
            skipped += 1
            continue

        texts.append(text)
        labels.append(label2id[intent])

    print(f"Loaded {len(texts)} samples, skipped {skipped}")

    from collections import Counter
    dist = Counter(labels)
    for label_id, count in sorted(dist.items()):
        print(f"  {id2label[label_id]}: {count} samples")

    return texts, labels

# ── Tokenizer ─────────────────────────────────────────────
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

# ── Metrics ───────────────────────────────────────────────
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    acc = accuracy_score(labels, preds)
    f1  = f1_score(labels, preds, average="weighted")
    return {"accuracy": acc, "f1": f1}

# ── Train ─────────────────────────────────────────────────
def train(dataset_path: str):
    texts, labels = load_data(dataset_path)

    # Split 80/20
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    print(f"\nTrain: {len(train_texts)} | Test: {len(test_texts)}")

    # HuggingFace datasets
    train_ds = Dataset.from_dict({"text": train_texts, "label": train_labels})
    test_ds  = Dataset.from_dict({"text": test_texts,  "label": test_labels})

    train_ds = train_ds.map(tokenize, batched=True)
    test_ds  = test_ds.map(tokenize,  batched=True)

    train_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    test_ds.set_format( "torch", columns=["input_ids", "attention_mask", "label"])

    # Load model
    model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(INTENTS),
    id2label=id2label,
    label2id=label2id,
    hidden_dropout_prob=0.2,
    attention_probs_dropout_prob=0.2)

    # Training args — fixed for newer HuggingFace versions
    args = TrainingArguments(
        output_dir=MODEL_SAVE,
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_dir="./logs",
        logging_steps=50,
        warmup_steps=100,
        weight_decay=0.01,
        report_to="none",
        dataloader_num_workers=0
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=test_ds,
        compute_metrics=compute_metrics,
    )

    print("\nStarting training...")
    trainer.train()

    # Final evaluation
    results = trainer.evaluate()
    print(f"\nFinal Accuracy: {results['eval_accuracy']:.4f}")
    print(f"Final F1 Score: {results['eval_f1']:.4f}")

    # Save
    os.makedirs(MODEL_SAVE, exist_ok=True)
    model.save_pretrained(MODEL_SAVE)
    tokenizer.save_pretrained(MODEL_SAVE)
    print(f"\nModel saved to {MODEL_SAVE}")

if __name__ == "__main__":
    train("../../data/intent_dataset_v3.json")