#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run static collection, database migrations, and seed sample catalog
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data
