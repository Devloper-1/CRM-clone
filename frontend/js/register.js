document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirm").value;

    if (password !== confirm) {
      alert("Passwords do not match!");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
      });

      if (res.ok) {
        alert("Registration successful! Please login.");
        window.location.href = "/frontend/login.html";
      } else {
        const error = await res.json();
        alert("Register failed: " + error.detail);
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
  });
});
