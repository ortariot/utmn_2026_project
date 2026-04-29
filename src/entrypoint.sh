#!/bin/bash
set -e

echo "Running database migrations..."
cd /app
MAX_RETRIES=30
RETRY_COUNT=0
until alembic upgrade head 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Failed to run migrations after $MAX_RETRIES attempts"
        alembic -c /app/alembic.ini upgrade head
        exit 1
    fi
    echo "Waiting for database to be ready... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

echo "Starting application..."
cd /app/src
exec uvicorn main:app --host 0.0.0.0 --port 8000
