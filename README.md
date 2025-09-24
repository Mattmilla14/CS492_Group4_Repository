# Bookstore Management System — CS492 Group 4

Frontend: static HTML/JS in `/frontend` (calls `http://localhost:5000/api`).  
Backend: Flask in `/backend` using SQLite (auto-created in `/backend/instance/bookstore.db`).

## Quick start
1. Python 3.10+ installed.
2. From repo root, start the backend:
   - Windows: `scripts\run_backend.bat`
   - macOS/Linux: `bash scripts/run_backend.sh`
3. In another terminal, start the frontend:
   - Windows: `scripts\run_frontend.bat`
   - macOS/Linux: `bash scripts/run_frontend.sh`
4. Visit `http://localhost:8080/`.

## Notes
- DB file is created automatically. No external accounts needed.
- Do not commit `backend/instance/` or any `*.db` files.
