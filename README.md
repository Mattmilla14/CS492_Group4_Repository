# Bookstore Management System — CS492 Group 4

Frontend: static HTML/JS in `/frontend` (served on port 8080).  
Backend: Flask in `/backend` (served on port 5000) using SQLite (`/backend/instance/bookstore.db`).  

---

## Project Overview
A simple bookstore management system supporting:
- User accounts (register, login, logout).
- Shopping cart and checkout.
- Inventory management (admin only).
- Notifications for low/out-of-stock items.
- Order tracking for users and admins.
- Password reset (demo-only, disclaimer in UI).

---

## Repository Structure
```
backend/        # Flask backend, models, routes, seed + utility scripts
frontend/       # HTML, CSS, JS static frontend
scripts/        # Helper scripts to run backend, frontend, seed admin, sync usernames
build/          # Convenience scripts for starting everything
```

---

## Requirements
- Python 3.10+  
- Node.js (optional, only if using npm for frontend tooling)  

Dependencies are listed in `backend/requirements.txt`.

---

## Quick Start (Windows)
1. Clone or download the repo.
2. Run `scripts\run_backend.bat` (this sets up venv, installs requirements, starts Flask).
3. Run `scripts\run_frontend.bat` (starts static server on port 8080).
4. Run `scripts\seed_admin.bat` (ensures admin@bookstore.com / admin123 exists).
5. Visit [http://localhost:8080](http://localhost:8080) in your browser.

### Mac/Linux
Use the `.sh` versions of the scripts in `/scripts/`.

---

## Demo Breakdown
**For Presentation Use:**
- **Racquel** presents main flow.
- **Larry, Matthew, Angel** add interjections during features:
  - Low stock notifications (admin only).
  - Order tracking (user and admin).
  - Password reset (shows disclaimer).

Scripts ensure the demo starts clean every time:
- `run_backend` → starts Flask and seeds sample users/books.  
- `run_frontend` → starts the UI.  
- `seed_admin` → ensures admin is available.  
- `sync_usernames` → keeps login consistency for demo accounts.  

---

## Default Accounts
- Admin: `admin@bookstore.com` / `admin123`
- User: `user@bookstore.com` / `user123`

---

## Notes
- Password reset is demo-only (token shown in JSON, no email).  
- Notifications appear only when stock is low/out.  
- Iteration backups and local DBs are ignored via `.gitignore`.
