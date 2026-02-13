#!/bin/bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Loading sample data..."
python manage.py load_sample_data || true

echo "Build completed successfully!"


