# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies specified in requirements.txt
RUN apt-get update && apt-get install -y gcc wget p7zip-full

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt  

# Create the data directory
RUN mkdir -p data

# Download the dataset zip file from Kaggle
RUN wget -o /tmp/archive.zip "https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/download?datasetVersionNumber=3"

# List out the files in /tmp along with their file types
RUN ls -l /tmp

# Extract the dataset zip file using jar command and copy extracted files into /app/data directory
# RUN jar xvf /tmp/archive.zip -C /tmp/ && mv /tmp/* /app/data/ && rm -rf /tmp/*
RUN 7z x /tmp/archive.zip -o/data/ && rm /tmp/archive.zip

# Copy the rest of the application code into the container at /app
COPY Book/ .

# List all files after copying for debugging purpose
RUN ls -l

# List the copied files for verification
RUN ls -l data/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
