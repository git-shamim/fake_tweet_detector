import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from utils.preprocess import clean_tweet
from utils.config import USE_FINETUNED_MODEL, MODEL_PATH

LABEL_MAP = {0: "🟥 Fake", 1: "🟩 Real"}

@st.cache_resource
def load_model():
    if USE_FINETUNED_MODEL:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    else:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=2)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

def predict_tweet(text):
    cleaned = clean_tweet(text)
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()
    return LABEL_MAP[pred], torch.softmax(logits, dim=1).tolist()[0]
