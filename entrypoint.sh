#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z clustersitter-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"
sleep 10
python /app/manage.py runserver --host 0.0.0.0