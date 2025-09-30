// ============================================================
// File: frontend/js/clients_ui.js
// Description: UI interactions for Clients page
// ============================================================

document.addEventListener("DOMContentLoaded", async () => {
  // ----------------------
  // Load clients table on page load
  // ----------------------
  await fetchClients();

  // ----------------------
  // Fill form on row click
  // ----------------------
  const table = document.getElementById("clientsTable");
  table.addEventListener("click", (e) => {
    const row = e.target.closest("tr");
    if (!row) return;

    const cells = row.querySelectorAll("td");
    if (cells.length < 5) return;

    document.getElementById("clientId").value = cells[0].textContent.trim();
    document.getElementById("userId").value = cells[1].textContent.trim();
    document.getElementById("name").value = cells[2].textContent.trim();
    document.getElementById("email").value = cells[3].textContent.trim();
    document.getElementById("phone").value =
      cells[4].textContent.trim() === "N/A" ? "" : cells[4].textContent.trim();
  });

  // ----------------------
  // Clear form
  // ----------------------
  document.getElementById("clearbtn").addEventListener("click", () => {
    document.getElementById("clientForm").reset();
  });

  // ----------------------
  // Sidebar toggle
  // ----------------------
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
});
