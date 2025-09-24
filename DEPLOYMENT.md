# Deployment and Demo Guide

This doc has a **Technical Runbook** and a **Simple Demo Breakdown**.

---

## Technical Runbook

### Run scripts
- Backend
  - Windows: `scripts\run_backend.bat`
  - Mac/Linux: `bash scripts/run_backend.sh`
- Frontend
  - Windows: `scripts\run_frontend.bat`
  - Mac/Linux: `bash scripts/run_frontend.sh`

### Endpoints (high level)
- `POST /api/register`  → `{ success, user, token }`
- `POST /api/login`     → `{ success, user, token }`
- `GET  /api/profile`   → `{ success, user }` (requires `Authorization: Bearer <token>`)
- `GET  /api/books`     → `{ success, data:[…] }`
- `GET  /api/books/:id` → `{ success, data:{…} }`
- `POST /api/books`     → admin only
- `PUT  /api/books/:id` → admin only
- `DELETE /api/books/:id` → admin only
- `POST /api/sales`     → creates a sale from cart items
- `GET  /api/sales`     → admin only
- `GET  /api/sales/user` → current user’s sales
- `GET  /api/sales/count` → `{ total_count, recent_sales }`

### Quick checks (browser)
- `http://localhost:5000/api/health` → JSON with `"success": true`
- `http://localhost:5000/api/books`  → JSON list

If something fails, watch the backend terminal for errors.

---

## Simple Demo Breakdown

1. **Open the store:** `http://localhost:8080` (home page visible).
2. **Login/Register:** Use a demo account or register a new one. Then log in.
3. **Find a book:** Search or open one from the catalog → show details (title/author/price/stock).
4. **Add to cart:** Add a book → open the cart page to show it appears.
5. **Change mind:** Remove it → cart updates.
6. **Checkout:** Add another book and complete checkout → show receipt/confirmation.
7. **(Optional) Inventory:** Add/edit/delete a book in Inventory → refresh list to confirm changes.

---

## Packaging (submission)
- Ensure `README.md`, `DEPLOYMENT.md`, `/backend`, `/frontend`, `/scripts`, `/build` present.
- Exclude `.venv`, `backend/instance/`, and any `*.db` files.
- Zip the repo as `CS492_GP4.ZIP`.
