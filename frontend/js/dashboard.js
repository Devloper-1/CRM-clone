// dashboard.js
document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("menu-toggle");

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });
});

// Login tocken 
document.addEventListener("DOMContentLoaded", () => {
  const token = sessionStorage.getItem("token");
  if (!token) {
    // if no token → send back to login
    window.location.href = "login.html";
  }
});

// Logout 
async function logout() {
  const token = sessionStorage.getItem("token");

  try {
    await fetch("http://127.0.0.1:8000/logout?token=" + token, {
      method: "POST"
    });
  } catch (err) {
    console.log("Error logging out:", err);
  }

  sessionStorage.clear();
  window.location.href = "login.html";
}
