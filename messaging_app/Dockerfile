# Use official Python 3.10 image as base
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Install system-level dependencies for PyGObject and other packages
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Default command to run the Django development server
# Adjust if you plan to use gunicorn or other production server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
