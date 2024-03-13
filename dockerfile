# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies specified in requirements.txt
RUN apt-get update && apt-get install -y gcc

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application code into the container at /app
COPY Book/ .

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
