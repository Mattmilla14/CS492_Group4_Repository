// === frontend/api.js ===
// Minimal helper so static HTML pages can call the backend.

(function () {
  var API_BASE = "http://localhost:5000/api"; // change if backend has no /api prefix

  function getToken() {
    try { return localStorage.getItem("jwt") || ""; } catch (_) { return ""; }
  }
  function setToken(t) {
    try { localStorage.setItem("jwt", t || ""); } catch (_) {}
  }
  function clearToken() {
    try { localStorage.removeItem("jwt"); } catch (_) {}
  }

  async function api(path, opts) {
    opts = opts || {};
    var method = (opts.method || "GET").toUpperCase();
    var headers = Object.assign({}, opts.headers || {});
    var token = getToken();
    if (token) headers["Authorization"] = "Bearer " + token;
    var body = opts.body;

    if (body && typeof body === "object" && !(body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(body);
    }

    var res = await fetch(API_BASE + path, { method, headers, body });
    if (!res.ok) {
      var errText = "";
      try { errText = await res.text(); } catch (_) {}
      throw new Error("API " + res.status + ": " + (errText || res.statusText));
    }
    var ct = res.headers.get("content-type") || "";
    return ct.includes("application/json") ? res.json() : null;
  }

  // Auth
  async function login(email, password) {
    var data = await api("/login", { method: "POST", body: { email: email, password: password } });
    if (data && data.access_token) setToken(data.access_token);
    return data;
  }
  async function register(email, password) {
    return api("/register", { method: "POST", body: { email: email, password: password } });
  }
  async function profile() {
    return api("/profile");
  }
  function logout() { clearToken(); }

  // Books
  function getBooks() { return api("/books"); }
  function getBook(id) { return api("/books/" + encodeURIComponent(id)); }
  function addBook(b) { return api("/books", { method: "POST", body: b }); }
  function editBook(id, b) { return api("/books/" + encodeURIComponent(id), { method: "PUT", body: b }); }
  function delBook(id) { return api("/books/" + encodeURIComponent(id), { method: "DELETE" }); }

  // Expose to pages
  window.API = {
    setBase(url) { API_BASE = url; },
    api, getToken, setToken, clearToken,
    login, register, profile, logout,
    getBooks, getBook, addBook, editBook, delBook
  };
})();
