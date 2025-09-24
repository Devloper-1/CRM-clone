// ================================
// CRM Users JS
// ================================
const API_BASE = "";  // Same host

// Fetch Users
function fetchUsers() {
  apiFetch(`${API_BASE}/users/`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("usersTable");
      container.innerHTML = "";

      if (data.length === 0) {
        container.innerHTML = `<tr><td colspan="4" class="text-center">No users found</td></tr>`;
        return;
      }

      data.forEach(user => {
        container.innerHTML += `
          <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.password ?? "N/A"}</td>
          </tr>`;
      });
    })
    .catch(err => {
      console.error("Error fetching users:", err);
      document.getElementById("usersTable").innerHTML =
        `<tr><td colspan="4" class="text-center text-red-600">Error loading users</td></tr>`;
    });
}

// Add User
function addUser() {
  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  apiFetch(`${API_BASE}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(res => res.json())
    .then(() => {
      alert("User added successfully!");
      fetchUsers();
    })
    .catch(err => console.error("Error adding user:", err));
}

// Update User
function updateUser() {
  const id = document.getElementById("userId").value;
  if (!id) return alert("Enter User ID to update");

  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  apiFetch(`${API_BASE}/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(res => res.json())
    .then(() => {
      alert("User updated successfully!");
      fetchUsers();
    })
    .catch(err => console.error("Error updating user:", err));
}

// Delete User
function deleteUser() {
  const id = document.getElementById("userId").value;
  if (!id) return alert("Enter User ID to delete");

  apiFetch(`${API_BASE}/users/${id}`, { method: "DELETE" })
    .then(() => {
      alert("User deleted successfully!");
      fetchUsers();
    })
    .catch(err => console.error("Error deleting user:", err));
}

window.fetchUsers = fetchUsers;
document.addEventListener("DOMContentLoaded", fetchUsers);

