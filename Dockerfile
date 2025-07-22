# Use an official Python image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies for pandas, numpy, and openpyxl
RUN apt-get update && \
    apt-get install -y gcc libpq-dev build-essential && \
    apt-get clean

# Install pip packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable for Flask (customise as needed)
ENV FLASK_APP app.py

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]