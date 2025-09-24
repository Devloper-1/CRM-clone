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
      window.location.href = "/frontend/login.html"; 
    } else {
      const error = await res.json();
      alert("❌ Logout failed: " + error.detail);
    }
  } catch (err) {
    alert("❌ Error: " + err.message);
  }
}
