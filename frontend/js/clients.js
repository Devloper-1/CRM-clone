// ================================
// CRM Client JS — Plan B (Relative Path)
// ================================

// Use relative path to work on any host (desktop, mobile, or Cloudflare Tunnel)
const API_BASE = "";  // Empty string = same host as frontend

// ================================
// Fetch All Clients
// ================================
function fetchClients() {
  fetch(`${API_BASE}/clients/`)
    .then(response => {
      if (!response.ok) throw new Error("Network error: " + response.statusText);
      return response.json();
    })
    .then(data => {
      const container = document.getElementById("clientsTable");
      if (!container) return console.error("❌ clientsTable element not found");

      // Clear previous table rows
      container.innerHTML = "";

      // Show message if no clients exist
      if (data.length === 0) {
        container.innerHTML = `<tr><td colspan="5" class="text-center">No clients found</td></tr>`;
        return;
      }

      // Populate table with client data
      data.forEach(client => {
        const row = `
          <tr>
            <td>${client.id}</td>
            <td>${client.user_id}</td>
            <td>${client.name}</td>
            <td>${client.email}</td>
            <td>${client.phone ?? "N/A"}</td>
          </tr>`;
        container.innerHTML += row;
      });
    })
    .catch(error => {
      console.error("Error fetching clients:", error);
      document.getElementById("clientsTable").innerHTML =
        `<tr><td colspan="5" class="text-center text-red-600">Error loading clients</td></tr>`;
    });
}

// ================================
// Add New Client
// ================================
function addClient() {
  const clientData = {
    user_id: document.getElementById("userId").value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
  };

  fetch(`${API_BASE}/clients`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(clientData),
  })
    .then(response => response.json())
    .then(() => {
      alert("Client added successfully!");
      fetchClients(); // Refresh table
    })
    .catch(error => console.error("Error adding client:", error));
}

// ================================
// Update Existing Client
// ================================
function updateClient() {
  const id = document.getElementById("clientId").value;
  if (!id) return alert("Please enter Client ID to update");

  const clientData = {
    user_id: document.getElementById("userId").value,
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    phone: document.getElementById("phone").value,
  };

  fetch(`${API_BASE}/clients/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(clientData),
  })
    .then(response => response.json())
    .then(() => {
      alert("Client updated successfully!");
      fetchClients(); // Refresh table
    })
    .catch(error => console.error("Error updating client:", error));
}

// ================================
// Delete Client
// ================================
function deleteClient() {
  const id = document.getElementById("clientId").value;
  if (!id) return alert("Please enter Client ID to delete");

  fetch(`${API_BASE}/clients/${id}`, { method: "DELETE" })
    .then(() => {
      alert("Client deleted successfully!");
      fetchClients(); // Refresh table
    })
    .catch(error => console.error("Error deleting client:", error));
}

// ================================
// Global Exports & DOM Ready
// ================================
window.fetchClients = fetchClients;
document.addEventListener("DOMContentLoaded", fetchClients);
