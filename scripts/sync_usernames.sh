#!/bin/bash
cd "$(dirname "$0")/../backend" || { echo "Backend folder not found"; exit 1; }
source .venv/bin/activate || { echo "Activate venv first (run run_backend.sh)"; exit 1; }
python sync_usernames.py
