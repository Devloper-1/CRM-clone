// ================================
// UI Interactions for Tasks
// ================================
document.addEventListener("DOMContentLoaded", () => {
  const table = document.getElementById("tasksTable");
  const form = document.getElementById("taskForm");

  // Row click → fill form
  table.addEventListener("click", e => {
    const row = e.target.closest("tr");
    if (!row) return;
    const cells = row.querySelectorAll("td");
    if (cells.length < 4) return;

    document.getElementById("taskId").value = cells[0].textContent.trim();
    document.getElementById("clientId").value = cells[1].textContent.trim();
    document.getElementById("description").value = cells[2].textContent.trim();
    document.getElementById("status").value = cells[3].textContent.trim();
  });

  // Clear form
  document.getElementById("clearbtn").addEventListener("click", () => {
    form.reset();
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
});
