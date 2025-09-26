// ================================
// CRM Clients UI Script
// ================================

// Run after DOM is fully loaded
document.addEventListener("DOMContentLoaded", async () => {
  // 1. Load clients table on page load
  await fetchClients();

  // 2. Attach click handler to table rows
  document.getElementById("clientsTable").addEventListener("click", (e) => {
    const row = e.target.closest("tr");   // find the clicked row
    if (!row) return;

    const cells = row.querySelectorAll("td"); // get all <td> inside this row
    if (cells.length < 5) return; // make sure enough cells

    // Fill the form fields
    document.getElementById("clientId").value = cells[0].textContent.trim();
    document.getElementById("userId").value   = cells[1].textContent.trim();
    document.getElementById("name").value     = cells[2].textContent.trim();
    document.getElementById("email").value    = cells[3].textContent.trim();
    document.getElementById("phone").value    =
      cells[4].textContent.trim() === "N/A" ? "" : cells[4].textContent.trim();
  });

  // 3. Clear button
  document.getElementById("clearbtn").addEventListener("click", () => {
    document.getElementById("clientForm").reset();
  });

  // 4. Sidebar toggle
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
