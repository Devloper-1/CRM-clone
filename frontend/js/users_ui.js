document.addEventListener("DOMContentLoaded", () => {
  // Fill form when row clicked
  document.getElementById("usersTable").addEventListener("click", (e) => {
    const row = e.target.closest("tr");
    if (!row) return;

    const cells = row.querySelectorAll("td");
    if (cells.length < 4) return;

    document.getElementById("userId").value   = cells[0].textContent.trim();
    document.getElementById("name").value     = cells[1].textContent.trim();
    document.getElementById("email").value    = cells[2].textContent.trim();
    document.getElementById("password").value = 
      cells[3].textContent.trim() === "N/A" ? "" : cells[3].textContent.trim();
  });

  // Clear form
  document.getElementById("clearbtn").addEventListener("click", () => {
    document.getElementById("userForm").reset();
  });

  // Sidebar toggle
  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");

  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("-translate-x-full");
    overlay.classList.toggle("hidden");
  });

  overlay.addEventListener("click", () => {
    sidebar.classList.add("-translate-x-full");
    overlay.classList.add("hidden");
  });

  // 👁️ Password toggle
  const passwordInput = document.getElementById("password");
  const toggleBtn = document.getElementById("togglePassword");

  toggleBtn.addEventListener("click", () => {
    const isHidden = passwordInput.type === "password";
    passwordInput.type = isHidden ? "text" : "password";
    toggleBtn.textContent = isHidden ? "🙈" : "👁️";
  });
});
