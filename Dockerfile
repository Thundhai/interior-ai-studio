FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and startup script
COPY src/ ./src/
COPY ui/ ./ui/
COPY *.py ./

# Environment variables
ENV PYTHONPATH=/app
# Security: Change this default key in production
ENV INTERIOR_AI_API_KEY=demo-changeme-not-secure

# Railway will set PORT dynamically - expose common port for reference
EXPOSE 8000

# Run application using Python startup script that handles Railway's PORT
CMD ["python", "start_server.py"]