import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .preprocess import clean_tweet

MODEL_NAME = "vinai/bertweet-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
model.eval()

LABEL_MAP = {0: "🟥 Fake", 1: "🟩 Real"}

def predict_tweet(text):
    cleaned = clean_tweet(text)
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()
    return LABEL_MAP[pred], torch.softmax(logits, dim=1).tolist()[0]
