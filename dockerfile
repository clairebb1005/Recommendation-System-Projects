# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies specified in requirements.txt
RUN apt-get update && apt-get install -y gcc wget fastjar

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

# Extract the dataset zip file
# RUN unzip /tmp/archive.zip -d /tmp/dataset
RUN jar xvf /tmp/archive.zip -C /tmp/data

# Copy the extracted files into the /app/Book/data directory
# RUN cp /tmp/dataset/* data/

# Copy the rest of the application code into the container at /app
# COPY Book/ .

# Expose port 8000 to the outside world
# EXPOSE 8000

# Command to run the application
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
