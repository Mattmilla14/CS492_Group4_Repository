#!/bin/bash
# scripts/seed_admin.sh
# Creates a default admin user if none exists (macOS/Linux).

# Navigate to backend relative to this script
cd "$(dirname "$0")/../backend" || { echo "Backend folder not found."; exit 1; }

# Activate venv
if [ -d ".venv" ]; then
  source .venv/bin/activate
else
  echo "No .venv found. Please run run_backend.sh or create venv first."
  exit 1
fi

# Run the seeder
python seed_admin.py
