FROM python:3.12-slim

# Ensure logs are visible
ENV PYTHONUNBUFFERED True

WORKDIR /app
COPY . .

# Install Gunicorn and other dependencies
RUN pip install --no-cache-dir flask gunicorn google-generativeai python-dotenv requests

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app