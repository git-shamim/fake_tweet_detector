FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y git && apt-get clean
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Preload model to local path (avoid Hugging Face calls)
RUN mkdir -p /app/models/bertweet_base && \
    python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
        AutoTokenizer.from_pretrained('vinai/bertweet-base', cache_dir='/app/models/bertweet_base'); \
        AutoModelForSequenceClassification.from_pretrained('vinai/bertweet-base', num_labels=2, cache_dir='/app/models/bertweet_base')"

EXPOSE 8080

ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    PYTHONPATH="${PYTHONPATH}:/app"

CMD ["streamlit", "run", "app.py", "--server.port=8080"]
