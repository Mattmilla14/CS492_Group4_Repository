@echo off
start cmd /k scripts\run_backend.bat
timeout /t 3 >nul
start cmd /k scripts\run_frontend.bat
