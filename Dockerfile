# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create cache directory
RUN mkdir -p /app/cache

# Copy the application code to the working directory
COPY app/ /app/app

# Set the PYTHONPATH environment variable so the app/ is treated as a module
ENV PYTHONPATH /app

# Expose port 8080 for the socket server
EXPOSE 8080

# Define the entry point for the Docker container
# CMD ["python", "app/main.py"]
# Use eventlet worker
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "250", "--worker-class", "eventlet", "app.main:app"]
