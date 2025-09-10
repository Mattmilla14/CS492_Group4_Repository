const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

const db = new sqlite3.Database(path.join(__dirname, "bookstore.db"));

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS items (
      isbn TEXT PRIMARY KEY,
      name TEXT,
      author TEXT,
      qty INTEGER,
      price REAL
    )
  `);
});

app.get("/api/health", (req, res) => {
  res.json({ ok: true });
});

app.get("/api/items", (req, res) => {
  db.all("SELECT * FROM items", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/api/items", (req, res) => {
  const { isbn, name, author, qty, price } = req.body;
  db.run(
    "INSERT INTO items (isbn, name, author, qty, price) VALUES (?,?,?,?,?)",
    [isbn, name, author, qty, price],
    (err) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ ok: true });
    }
  );
});

app.put("/api/items/:isbn", (req, res) => {
  const { isbn } = req.params;
  const { name, author, qty, price } = req.body;
  db.run(
    "UPDATE items SET name=?, author=?, qty=?, price=? WHERE isbn=?",
    [name, author, qty, price, isbn],
    (err) => {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ ok: true });
    }
  );
});

app.delete("/api/items/:isbn", (req, res) => {
  const { isbn } = req.params;
  db.run("DELETE FROM items WHERE isbn=?", [isbn], (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API running at http://localhost:${PORT}`);
});
