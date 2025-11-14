#!/bin/bash
set -e

echo "====================================="
echo "SOaC Framework - Railway Deployment"
echo "====================================="

# Railway provides DATABASE_URL automatically for PostgreSQL
# Extract database connection details
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL not set!"
    exit 1
fi

echo "✓ Database URL configured"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
max_attempts=30
attempt=0

# Extract host and port from DATABASE_URL
# Format: postgresql://user:pass@host:port/db
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
    echo "WARNING: Could not parse database host/port, skipping connection check"
else
    until pg_isready -h $DB_HOST -p $DB_PORT > /dev/null 2>&1; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo "ERROR: Database not ready after $max_attempts attempts"
            exit 1
        fi
        echo "  Attempt $attempt/$max_attempts - PostgreSQL is unavailable, waiting..."
        sleep 2
    done
    echo "✓ PostgreSQL is ready!"
fi

# Initialize database with sample data
echo "Initializing database..."
if python -m app.init_db; then
    echo "✓ Database initialized successfully"
else
    echo "⚠ Database initialization failed, but continuing..."
fi

# Use PORT environment variable provided by Railway (defaults to 8000)
export PORT=${PORT:-8000}
echo "✓ Starting server on port $PORT"

# Start application with Gunicorn for production
echo "====================================="
echo "Starting SOaC Framework Backend API"
echo "====================================="

# Use gunicorn with uvicorn workers for production
exec gunicorn app.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
