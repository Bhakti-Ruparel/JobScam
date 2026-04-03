FROM python:3.11-slim

# Install Tesseract + system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Tesseract data path
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
ENV PORT=8000

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project (model downloads at runtime, not baked in)
COPY backend/ ./backend/
COPY frontend/ ./frontend/

ENV PYTHONPATH=/app

CMD uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
