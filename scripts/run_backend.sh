#!/bin/bash
# scripts/run_backend.sh
# One-click backend launcher for macOS/Linux.

# Move to backend directory relative to this script
cd "$(dirname "$0")/../backend" || { echo "Backend folder not found."; exit 1; }

# Create venv if missing
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv || python -m venv .venv || { echo "Failed to create venv"; exit 1; }
fi

# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate || { echo "Failed to activate venv"; exit 1; }

# Install requirements
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt ..."
  pip install --disable-pip-version-check -q -r requirements.txt || { echo "pip install failed"; exit 1; }
else
  echo "requirements.txt not found. Installing core deps..."
  pip install --disable-pip-version-check -q flask flask_sqlalchemy flask_bcrypt pyjwt flask-cors || { echo "pip install failed"; exit 1; }
fi

export FLASK_APP=app.py
echo "Starting backend at http://localhost:5000 ..."
flask run
