// ================================
// CRM Clients JS — Modern Approach
// ================================

// ------------------------
// Fetch All Clients
// ------------------------
async function fetchClients() {
  try {
    const data = await apiFetch("/clients"); // uses token automatically

    const container = document.getElementById("clientsTable");
    if (!container) return console.error("❌ clientsTable element not found");

    container.innerHTML = "";

    if (!data || data.length === 0) {
      container.innerHTML = `<tr><td colspan="5" class="text-center">No clients found</td></tr>`;
      return;
    }

    data.forEach(client => {
      container.innerHTML += `
        <tr>
          <td>${client.id}</td>
          <td>${client.user_id}</td>
          <td>${client.name}</td>
          <td>${client.email}</td>
          <td>${client.phone ?? "N/A"}</td>
        </tr>`;
    });
  } catch (err) {
    console.error("Error fetching clients:", err);
    document.getElementById("clientsTable").innerHTML =
      `<tr><td colspan="5" class="text-center text-red-600">Error loading clients</td></tr>`;
  }
}

// ------------------------
// Add New Client
// ------------------------
async function addClient() {
  const clientData = {
    user_id: document.getElementById("userId").value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
  };

  try {
    await apiFetch("/clients", {
      method: "POST",
      body: JSON.stringify(clientData),
    });
    alert("Client added successfully!");
    fetchClients();
  } catch (err) {
    console.error("Error adding client:", err);
  }
}

// ------------------------
// Update Existing Client
// ------------------------
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
    await apiFetch(`/clients/${id}`, {
      method: "PUT",
      body: JSON.stringify(clientData),
    });
    alert("Client updated successfully!");
    fetchClients();
  } catch (err) {
    console.error("Error updating client:", err);
  }
}

// ------------------------
// Delete Client
// ------------------------
async function deleteClient() {
  const id = document.getElementById("clientId").value;
  if (!id) return alert("Please enter Client ID to delete");

  try {
    await apiFetch(`/clients/${id}`, { method: "DELETE" });
    alert("Client deleted successfully!");
    fetchClients();
  } catch (err) {
    console.error("Error deleting client:", err);
  }
}

// ------------------------
// Expose functions globally
// ------------------------
window.fetchClients = fetchClients;
window.addClient = addClient;
window.updateClient = updateClient;
window.deleteClient = deleteClient;

document.addEventListener("DOMContentLoaded", fetchClients);
