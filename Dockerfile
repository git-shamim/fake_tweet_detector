FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y git && apt-get clean
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Preload BERTweet model/tokenizer at build time
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('vinai/bertweet-base'); \
    AutoModelForSequenceClassification.from_pretrained('vinai/bertweet-base', num_labels=2)"

EXPOSE 8080

ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false

CMD ["streamlit", "run", "app.py", "--server.port=8080"]
