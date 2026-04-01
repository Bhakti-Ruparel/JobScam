FROM python:3.10-slim

# Install Tesseract + system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project (includes backend/models/)
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Set Python path
ENV PYTHONPATH=/app

# Dynamic port for Railway/Render/Fly.io
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
