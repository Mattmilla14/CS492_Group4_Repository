# 📦 Bookstore — Week 2 Backend + Dual-Mode Frontend (Deployment & Demo)

This guide explains how to run, deploy, and demo our bookstore project.  
It includes everything needed for teammates, professor, or graders to see the system working in both **Local** and **Server** modes.

---

## 📁 Project Structure

```text
CS492_Group4_Repository/
├── cart.html
├── inventory.html
├── store.html
├── README.md
└── week2/
    ├── DEPLOYMENT.md
    ├── backend/
    │   ├── server.js
    │   └── package.json
    ├── inventory.html
    └── shop.html
```

---

## ⚙️ Backend Setup

The backend lives in `week2/backend/`.

- `server.js` → Express + SQLite API  
- `package.json` → dependencies (`express`, `sqlite3`, `cors`)  

---

## ▶️ Running Locally

```bash
cd week2/backend
npm install
npm start
```

- API runs at: **http://localhost:3000**  
- Health check: [http://localhost:3000/api/health](http://localhost:3000/api/health) → `{ ok: true }`  
- Items list: [http://localhost:3000/api/items](http://localhost:3000/api/items)  

👉 Then open `week2/inventory.html` (Admin) or `week2/shop.html` (Shop).  
The **Mode badge** will flip to **Server** automatically if the backend is running.

---

## ☁️ Free Cloud Deploy

```text
1. Push week2/backend/ to its own repo.
2. In Render (https://render.com):
   - New → Web Service → connect repo.
   - Build Command: npm install
   - Start Command: node server.js
3. Deploy → copy public URL (e.g. https://bookstore-backend.onrender.com)
```

Alternative hosts: [https://railway.app](https://railway.app), Fly.io, etc.  

⚠️ Free tiers reset DB on redeploy. Use **Load Sample Data** in Admin to reseed quickly.

---

## 🔗 Pointing Frontend to Backend

**Temporary (via browser console):**

```js
window.BOOKSTORE_API = "https://your-backend.onrender.com";
localStorage.setItem("BOOKSTORE_API_DEFAULT", window.BOOKSTORE_API);
location.reload();
```

**Permanent (hard-coded):**

```js
window.BOOKSTORE_API = "https://your-backend.onrender.com";
```

Update this line in `week2/inventory.html` and `week2/shop.html`.

---

## 🎤 Demo Script (for 4 presenters)

```text
1. Admin (Local)
   - Open Admin → click Load Sample Data → show items, edit, sort, export.

2. Switch to Server
   - Run console snippet with backend URL → reload → badge shows Server.
   - Click Sync from Server → data persists.

3. Shop (Server)
   - Open Shop → see catalog from server.
   - Add to cart → checkout → stock decrements on server.
   - Back in Admin → Sync → quantities update.

4. Offline/Resilience
   - Clear window.BOOKSTORE_API → reload → badge shows Local.
   - Show app still works with local storage.
```

---

## 🛠️ Troubleshooting

```text
- CORS → backend already uses cors(). If blocked, ensure HTTPS frontend calls HTTPS backend.
- Badge won’t flip → test /api/health. If 500 or no response, backend isn’t running.
- DB wiped → reseed with Load Sample Data.
- Port conflict locally → change PORT in server.js.
```

---

✅ End of Guide
