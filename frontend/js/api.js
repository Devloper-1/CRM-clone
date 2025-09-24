// =============================
// API Helper (reusable)
// =============================
async function apiFetch(url, options = {}) {
  const token = sessionStorage.getItem("token");

  if (!token) {
    window.location.href = "/frontend/login.html";
    return;
  }

  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (res.status === 401) {
    sessionStorage.clear();
    window.location.href = "/frontend/login.html";
    return;
  }

  return res.json();
}

// =============================
// Logout helper
// =============================
function logout() {
  sessionStorage.clear();
  window.location.href = "/frontend/login.html";
}
