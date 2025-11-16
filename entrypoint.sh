#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 config.wsgi:application
