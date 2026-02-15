#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Creating instance directory..."
mkdir -p instance

echo "==> Initializing database..."
python3 init_db.py

if [ $? -eq 0 ]; then
    echo "==> Build completed successfully!"
else
    echo "==> ERROR: Database initialization failed!"
    exit 1
fi
