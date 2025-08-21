# Use Python 3.11 to avoid FastAPI+pydantic v1 issues on Python 3.13
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (add if needed for psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
