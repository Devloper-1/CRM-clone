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
      sessionStorage.setItem("token", data.access_token);
      sessionStorage.setItem("userEmail", email);
      window.location.href = "/frontend/dashboard.html";
    } else {
      const error = await res.json();
      alert("Login failed: " + error.detail);
    }
  } catch (err) {
    alert("Error: " + err.message);
  }
}


  // Run after DOM is loaded
  document.addEventListener("DOMContentLoaded", () => {
    setupToggle("togglePassword", "password");
  });

