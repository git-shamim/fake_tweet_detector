import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from utils.preprocess import clean_tweet
from utils.config import USE_FINETUNED_MODEL, MODEL_PATH

@st.cache_resource
def load_model():
    if USE_FINETUNED_MODEL:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    else:
        tokenizer = AutoTokenizer.from_pretrained("vinai/bertweet-base")
        model = AutoModelForSequenceClassification.from_pretrained("vinai/bertweet-base", num_labels=2)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

def predict_tweet(text):
    cleaned = clean_tweet(text)
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1).tolist()[0]
        fake_prob, real_prob = probs

    # Interpret result based on real class probability
    if real_prob > 0.60:
        label = "🟩 Very likely genuine"
    elif real_prob < 0.40:
        label = "🟥 Very likely fake"
    else:
        label = "🟧 Uncertain or unclear"

    return label, probs
