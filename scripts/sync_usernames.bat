@echo off
cd /d "%~dp0..\backend"
call .venv\Scripts\activate
python sync_usernames.py
pause