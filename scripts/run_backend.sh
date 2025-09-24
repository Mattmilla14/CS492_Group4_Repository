#!/usr/bin/env bash
set -e
python -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip >/dev/null 2>&1 || true
pip install -r backend/requirements.txt
export FLASK_APP=backend/app.py
python backend/app.py
