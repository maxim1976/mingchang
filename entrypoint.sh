#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating cache table..."
python manage.py createcachetable

echo "Generating ImageKit cache files..."
python manage.py generateimages

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 config.wsgi:application
