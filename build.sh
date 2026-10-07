#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run static collection, database migrations, and seed sample catalog
python ecommerce/manage.py collectstatic --no-input
python ecommerce/manage.py migrate
python ecommerce/manage.py seed_data
