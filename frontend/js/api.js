// ============================================================
// File: /frontend/js/api.js
// Description: Helper functions for API requests with JWT support.
//              Automatically handles token validation, logout, and JSON parsing.
// ============================================================

// ----------------------
// API FETCH WITH JWT
// ----------------------
async function apiFetch(url, options = {} , raw = false) {
  const token = sessionStorage.getItem("token");
  if (!token) {
    // Redirect to login if no token
    sessionStorage.setItem("redirect", window.location.pathname);
    window.location.href = "/frontend/login.html";
    return;
  }

  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (res.status === 401) {
    // Unauthorized → logout
    sessionStorage.clear();
    alert("⚠️ Session expired. Please log in again.");
    window.location.href = "/frontend/login.html";
    return;
  }

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  // Return raw response if requested (for CSV or files)
  if (raw) return res;

  return res.json();
}

// ----------------------
// LOGOUT
// ----------------------
function logout() {
  sessionStorage.clear();
  window.location.href = "/frontend/login.html";
}

// ----------------------
// EXPORT TO GLOBAL SCOPE
// ----------------------
window.apiFetch = apiFetch;
window.logout = logout;

console.log("✅ api.js loaded and apiFetch ready");
