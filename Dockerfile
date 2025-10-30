"""
Production Deployment Guide for Interior AI Studio
"""

# Option 1: Docker Deployment (Recommended)
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY ui/ ./ui/
COPY *.py ./

# Environment variables
ENV PYTHONPATH=/app
ENV INTERIOR_AI_API_KEY=changeme

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]