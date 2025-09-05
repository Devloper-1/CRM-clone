// dashboard.js
document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("menu-toggle");

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });
});

const token = sessionStorage.getItem("token");

// If not logged in → redirect
if (!token) {
  window.location.href = "login.html";
}

document.getElementById("logoutBtn").addEventListener("click", async () => {
  try {
    await fetch("http://127.0.0.1:8000/auth/logout?token=" + token, {
      method: "POST"
    });
  } catch (err) {
    console.log("Error logging out:", err);
  }

  sessionStorage.removeItem("token");  // remove token
  window.location.href = "login.html"; // redirect
});
