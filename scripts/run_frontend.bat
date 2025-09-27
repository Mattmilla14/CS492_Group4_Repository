@echo off
cd /d "%~dp0..\frontend"

echo Starting frontend server at http://localhost:8080 ...
python -m http.server 8080
