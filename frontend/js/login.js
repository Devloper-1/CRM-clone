// login.js
// ----------------------
// Handles login page
// ----------------------
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) throw new Error("Invalid credentials");

    const data = await res.json();
    sessionStorage.setItem("token", data.token);

    // redirect after login
    window.location.href = sessionStorage.getItem("redirect") || "/frontend/dashboard.html";
    sessionStorage.removeItem("redirect");

  } catch (err) {
    alert("Login failed: " + err.message);
  }
}

// Password toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("togglePassword");
  const pwd = document.getElementById("password");
  toggle.addEventListener("click", () => {
    pwd.type = pwd.type === "password" ? "text" : "password";
  });
});
