#!/bin/sh
set -e

# Run database migrations
echo "==> Running database migrations..."
python manage.py migrate --noinput

# Ensure seed data is loaded
echo "==> Ensuring stories and seed data are populated..."
python manage.py seed_stories || true

# Start Gunicorn server listening on Cloud Run $PORT (defaults to 8080)
echo "==> Starting Gunicorn on 0.0.0.0:${PORT:-8080}..."
exec gunicorn storyforge.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
