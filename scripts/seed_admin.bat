@echo off
REM Launch from anywhere; switch into backend first
cd /d "%~dp0..\backend"
call .venv\Scripts\activate
python seed_admin.py
pause