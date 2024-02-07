# Use a slim Python image
FROM python:3.11-slim-buster

# Set work directory
WORKDIR /project/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for PostgreSQL and image processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    # Clean up to reduce image size
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Copy Pipfile and Pipfile.lock to install Python dependencies
COPY Pipfile Pipfile.lock /project/
RUN pipenv install --system --dev

# Copy the rest of the application
COPY . /project/
