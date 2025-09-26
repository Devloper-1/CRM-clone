// api.js
// ----------------------
// Helper for API requests
// ----------------------
async function apiFetch(url, options = {}) {
  const token = sessionStorage.getItem("token");
  if (!token) {
    // redirect to login if no token
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
    // unauthorized → logout
    sessionStorage.clear();
    window.location.href = "/frontend/login.html";
    return;
  }

  return res.json();
}

// Logout function
function logout() {
  sessionStorage.clear();
  window.location.href = "/frontend/login.html";
}
