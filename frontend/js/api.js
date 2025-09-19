// =============================
// API Helper (reusable)
// =============================
async function apiFetch(url, options = {}) {
  const token = sessionStorage.getItem("token");

  // If no token → force login
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  const res = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${token}`,   // always send token
      "Content-Type": "application/json",   // default for POST/PUT
    },
  });

  if (res.status === 401) {
    // Token invalid/expired → log out
    sessionStorage.clear();
    window.location.href = "login.html";
    return;
  }

  return res.json();
}

// =============================
// Logout helper
// =============================
function logout() {
  sessionStorage.clear();
  window.location.href = "login.html";
}
