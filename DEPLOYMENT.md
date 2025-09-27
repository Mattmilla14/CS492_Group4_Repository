# Deployment Guide — Bookstore Management System

---

## Setup Instructions

### Prerequisites
- Python 3.10+ installed.
- Git installed.
- (Optional) Node.js for frontend builds, not required for demo.

---

### Backend Setup
1. Navigate to `/backend`.
2. Ensure `requirements.txt` is present.
3. Run backend:
   - **Windows**: `scripts\run_backend.bat`
   - **Mac/Linux**: `./scripts/run_backend.sh`

This will:
- Create a virtual environment.
- Install all dependencies from `requirements.txt`.
- Start Flask at `http://127.0.0.1:5000`.

---

### Frontend Setup
1. Navigate to `/frontend`.
2. Run:
   - **Windows**: `scripts\run_frontend.bat`
   - **Mac/Linux**: `./scripts/run_frontend.sh`

This will:
- Serve frontend at `http://localhost:8080`.

---

### Admin Seeding
To ensure the demo admin account exists:
- **Windows**: `scripts\seed_admin.bat`
- **Mac/Linux**: `./scripts/seed_admin.sh`

Default seeded account:
- Email: `admin@bookstore.com`
- Password: `admin123`

---

### Sync Usernames
For consistency across demo accounts:
- **Windows**: `scripts\sync_usernames.bat`
- **Mac/Linux**: `./scripts/sync_usernames.sh`

---

## Simple Demo Breakdown
1. **Start Backend** → `run_backend`  
   - Seeds books, users, and ensures DB is created.  

2. **Start Frontend** → `run_frontend`  
   - Opens app at [http://localhost:8080](http://localhost:8080).  

3. **Seed Admin** → `seed_admin`  
   - Confirms `admin@bookstore.com` / `admin123` exists.  

4. **Login Paths**:  
   - Admin: can view inventory, notifications, all orders.  
   - User: can shop, checkout, view order history.  

---

## Demo Roles
- **Racquel**: primary walkthrough.  
- **Larry, Matthew, Angel**: add short interjections for key features (notifications, order tracking, password reset disclaimer).  

---

## Known Limitations
- Password reset = demo only (token shown in JSON).  
- No external email service.  
- Inventory updates are basic, no bulk import.
