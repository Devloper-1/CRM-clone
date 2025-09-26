// users.js
// ----------------------
// API CRUD for Users
// ----------------------

// Fetch & display all users
async function fetchUsers() {
  try {
    const users = await apiFetch("/users");
    const table = document.getElementById("usersTable");
    table.innerHTML = "";

    if (!users || users.length === 0) {
      table.innerHTML = `<tr><td colspan="4" class="px-4 py-3 text-center text-gray-500">No users found</td></tr>`;
      return;
    }

    users.forEach(u => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="border px-4 py-2">${u.id}</td>
        <td class="border px-4 py-2">${u.name}</td>
        <td class="border px-4 py-2">${u.email}</td>
        <td class="border px-4 py-2">N/A</td>
      `;
      table.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching users:", err);
    alert("Error fetching users");
  }
}

// Add user
async function addUser() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    await apiFetch("/users/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password }),
    });
    alert("User added successfully!");
    fetchUsers();
  } catch (err) {
    console.error(err);
    alert("Error adding user");
  }
}

// Update user
async function updateUser() {
  const id = document.getElementById("userId").value;
  if (!id) return alert("Enter User ID");

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    await apiFetch(`/users/${id}`, {
      method: "PUT",
      body: JSON.stringify({ name, email, password }),
    });
    alert("User updated successfully!");
    fetchUsers();
  } catch (err) {
    console.error(err);
    alert("Error updating user");
  }
}

// Delete user
async function deleteUser() {
  const id = document.getElementById("userId").value;
  if (!id) return alert("Enter User ID");

  try {
    await apiFetch(`/users/${id}`, { method: "DELETE" });
    alert("User deleted successfully!");
    fetchUsers();
  } catch (err) {
    console.error(err);
    alert("Error deleting user");
  }
}

// Load users on page load
document.addEventListener("DOMContentLoaded", fetchUsers);
