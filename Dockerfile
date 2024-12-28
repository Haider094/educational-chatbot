# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    curl \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install requirements
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir "tokenizers==0.13.3" && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY app/ /app/app
COPY .env /app/.env

# Set the PYTHONPATH environment variable
ENV PYTHONPATH /app

# Expose port 8080 for the socket server
EXPOSE 8080

# Use eventlet worker
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "250", "--worker-class", "eventlet", "app.main:app"]
