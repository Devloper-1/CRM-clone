async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (res.ok) {
      const data = await res.json();
      sessionStorage.setItem("token", data.token);
      alert("✅ Login successful!");
      window.location.href = "dashboard.html";
    } else {
      const error = await res.json();
      alert("❌ Login failed: " + error.detail);
    }
  } catch (err) {
    alert("❌ Error: " + err.message);
  }
}

async function logout() {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("⚠️ No token found!");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/logout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token })
    });

    if (res.ok) {
      sessionStorage.clear();
      alert("✅ Logged out!");
      window.location.href = "login.html";
    } else {
      const error = await res.json();
      alert("❌ Logout failed: " + error.detail);
    }
  } catch (err) {
    alert("❌ Error: " + err.message);
  }
}
