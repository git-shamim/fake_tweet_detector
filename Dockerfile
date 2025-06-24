# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Prevent Streamlit from asking user input
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_HOME="/app/app" \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ENABLEXSRS=false

# Launch the Streamlit app
CMD ["streamlit", "run", "app/app.py"]
