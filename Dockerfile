# ==============================================================================
# StoryForge - Production Dockerfile for Google Cloud Run
# ==============================================================================
FROM python:3.11-slim

# Set environment variables for Python & Django
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PORT=8080 \
    DJANGO_SETTINGS_MODULE=storyforge.settings

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . /app/

# Normalize line endings and make entrypoint executable (fixes Windows CRLF issues)
RUN sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Collect static files into STATIC_ROOT using WhiteNoise
RUN python manage.py collectstatic --noinput

# Run initial migrations and seed stories so the entire website is pre-populated inside the container
RUN python manage.py migrate --noinput && \
    python manage.py seed_stories || true

# Expose port (Google Cloud Run passes $PORT, defaults to 8080)
EXPOSE 8080

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
