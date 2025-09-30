// ============================================================
// File: frontend/js/clients.js
// Description: API CRUD operations for Clients (JWT protected)
// ============================================================

// ----------------------
// CLIENT FETCH ALL
// ----------------------
async function fetchClients() {
  try {
    const data = await apiFetch("/clients");
    const container = document.getElementById("clientsTable");
    if (!container) return console.error("❌ clientsTable element not found");

    container.innerHTML = "";

    if (!data || data.length === 0) {
      container.innerHTML = `<tr><td colspan="5" class="text-center">No clients found</td></tr>`;
      return;
    }

    data.forEach(client => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="border px-4 py-2">${client.id}</td>
        <td class="border px-4 py-2">${client.user_id}</td>
        <td class="border px-4 py-2">${client.name}</td>
        <td class="border px-4 py-2">${client.email}</td>
        <td class="border px-4 py-2">${client.phone ?? "N/A"}</td>
      `;
      container.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching clients:", err);
    document.getElementById("clientsTable").innerHTML =
      `<tr><td colspan="5" class="text-center text-red-600">Error loading clients</td></tr>`;
  }
}

// ----------------------
// CLIENT ADD
// ----------------------
async function addClient() {
  const clientData = {
    user_id: document.getElementById("userId").value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
  };

  try {
    await apiFetch("/clients", { method: "POST", body: JSON.stringify(clientData) });
    alert("Client added successfully!");
    fetchClients();
  } catch (err) {
    console.error("Error adding client:", err);
    alert("Error adding client");
  }
}

// ----------------------
// CLIENT UPDATE
// ----------------------
async function updateClient() {
  const id = document.getElementById("clientId").value;
  if (!id) return alert("Please enter Client ID to update");

  const clientData = {
    user_id: document.getElementById("userId").value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
  };

  try {
    await apiFetch(`/clients/${id}`, { method: "PUT", body: JSON.stringify(clientData) });
    alert("Client updated successfully!");
    fetchClients();
  } catch (err) {
    console.error("Error updating client:", err);
    alert("Error updating client");
  }
}

// ----------------------
// CLIENT DELETE
// ----------------------
async function deleteClient() {
  const id = document.getElementById("clientId").value;
  if (!id) return alert("Please enter Client ID to delete");

  try {
    await apiFetch(`/clients/${id}`, { method: "DELETE" });
    alert("Client deleted successfully!");
    fetchClients();
  } catch (err) {
    console.error("Error deleting client:", err);
    alert("Error deleting client");
  }
}

// ----------------------
// Expose functions globally
// ----------------------
window.fetchClients = fetchClients;
window.addClient = addClient;
window.updateClient = updateClient;
window.deleteClient = deleteClient;
