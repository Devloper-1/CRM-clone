async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (res.ok) {
    const data = await res.json();
    sessionStorage.setItem("token", data.token);
    sessionStorage.setItem("userEmail", email);
    alert("Login successful!");
    window.location.href = "dashboard.html";
  } else {
    const error = await res.json();
    alert("Login failed: " + error.detail);
  }
}

 
  // Generic toggle function
  function setupToggle(buttonId, inputId) {
    const toggleBtn = document.getElementById(buttonId);
    const input = document.getElementById(inputId);

    toggleBtn.addEventListener("click", () => {
      if (input.type === "password") {
        input.type = "text";
        toggleBtn.textContent = "🙈"; // Hide
      } else {
        input.type = "password";
        toggleBtn.textContent = "👁️"; // Show
      }
    });
  }

  // Run after DOM is loaded
  document.addEventListener("DOMContentLoaded", () => {
    setupToggle("togglePassword", "password");
  });

