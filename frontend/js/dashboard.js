document.addEventListener("DOMContentLoaded", () => {
  const token = sessionStorage.getItem("token");
  if (!token) window.location.href = "/frontend/login.html";

  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("menu-toggle");
  const overlay = document.getElementById("overlay");

  toggleBtn?.addEventListener("click", () => {
    sidebar.classList.toggle("-translate-x-full");
    overlay.classList.toggle("hidden");
  });

  overlay?.addEventListener("click", () => {
    sidebar.classList.add("-translate-x-full");
    overlay.classList.add("hidden");
  });

  const logoutBtn = document.getElementById("logoutBtn");
  logoutBtn?.addEventListener("click", logout); // Use global logout
});
