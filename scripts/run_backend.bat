@echo off
setlocal
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip >nul
pip install -r backend\requirements.txt
set FLASK_APP=backend\app.py
python backend\app.py
