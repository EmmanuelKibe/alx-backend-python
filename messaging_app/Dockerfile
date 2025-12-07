# Use Python 3.10 slim as instructed
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose default Django port
EXPOSE 8000

# Default command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



