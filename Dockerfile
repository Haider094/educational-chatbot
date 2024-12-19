# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Rust and Cargo, and ensure the environment is sourced
RUN apt-get update && apt-get install -y \
    curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . $HOME/.cargo/env \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY app/ /app/app
COPY .env /app/.env

# Set the PYTHONPATH environment variable so the app/ is treated as a module
ENV PYTHONPATH /app

# Expose port 8080 for the socket server
EXPOSE 8080

# Define the entry point for the Docker container
# CMD ["python", "app/main.py"]
# Use eventlet worker
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "250", "--worker-class", "eventlet", "app.main:app"]
