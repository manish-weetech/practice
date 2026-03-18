#!/bin/bash

# Exit on error
set -e

echo "Waiting for database to be ready..."
# Use python to check database connectivity
python << END
import sys
import psycopg2
import time
import os

db_url = os.environ.get("DB_CONNECTION")
while True:
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        break
    except Exception as e:
        print(f"Waiting for database... {e}")
        time.sleep(1)
END

echo "Database is ready! Running migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
