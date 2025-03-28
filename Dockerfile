# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    git && \
    apt-get clean && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./Scripts /app/Scripts

# Expose the port that the application will run on
EXPOSE 3000

# Command to run BentoML service
CMD ["bentoml", "serve", "Scripts.serviceNLP:svc", "--port", "3000"]
