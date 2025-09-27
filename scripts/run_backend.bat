@echo off
cd /d "%~dp0..\backend"

REM Create venv if not present
if not exist .venv (
  echo Creating virtual environment...
  py -m venv .venv
)

REM Activate venv
call .venv\Scripts\activate

REM Install requirements
echo Installing dependencies...
pip install --disable-pip-version-check -q -r requirements.txt

REM Set Flask app and run
set FLASK_APP=app.py
echo Starting backend server...
flask run
