# Use a Python base image with FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory
WORKDIR /app

# Copy the application code and dependencies
COPY main.py /app/
COPY requirements.txt /app/
COPY my_lib /app/my_lib

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt