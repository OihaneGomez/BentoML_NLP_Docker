# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Configure pip to use a mirror for package installation, in case of hash mismatches from the default index
RUN pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple

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

# Set environment variables
ENV PYTHONPATH="/app/Scripts"
ENV BENTOML_HOME=/app

# Expose the port that the application will run on
EXPOSE 3000

# Command to run BentoML service
CMD ["bentoml", "serve", "Scripts.serviceNLP:svc", "--port", "3000"]
