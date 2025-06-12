#!/bin/sh

set -e

# collect all static files to the root directory
python manage.py collectstatic --no-input

gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:8000 &

wait