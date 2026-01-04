FROM python:3.11-slim

# System dependencies for PDF processing and native builds (faiss, etc.)
RUN apt-get update \ 
    && apt-get install -y --no-install-recommends build-essential poppler-utils \ 
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \ 
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy application code
COPY . .

ENV PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Use gunicorn to serve the Flask app factory
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:8080", "--workers", "3"]
