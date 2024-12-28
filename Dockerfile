# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and Rust
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    cmake \
    pkg-config \
    && rm -rf /var/lib/apt/lists/* \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python packages in two steps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir tokenizers==0.13.3 && \
    pip install --no-cache-dir -r requirements.txt

# Create directory for SQLite database
RUN mkdir -p /app/data

# Copy the application code to the working directory
COPY app/ /app/app
COPY .env /app/.env

# Set the PYTHONPATH environment variable so the app/ is treated as a module
ENV PYTHONPATH /app

# Expose port 8080 for the socket server
EXPOSE 8080

# Change volume mount point
VOLUME ["/app/data"]

# Use eventlet worker
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "250", "--worker-class", "eventlet", "app.main:app"]
