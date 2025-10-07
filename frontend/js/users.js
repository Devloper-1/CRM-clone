// ============================================================
// File: /frontend/js/users.js
// Description: Handles all API CRUD operations for Users.
//              JWT protected, communicates with backend.
// ============================================================

// ----------------------
// FETCH ALL USERS
// ----------------------
async function fetchUsers() {
  try {
    const users = await apiFetch("/users/");
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

// ----------------------
// USER ADD
// ----------------------
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

// ----------------------
// USER UPDATE
// ----------------------
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

// ----------------------
// USER DELETE
// ----------------------
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

// ----------------------
// EXPORT Users TO CSV
// ----------------------
async function  exportusers() {
  alert("✅ Export button clicked!");

  const token = sessionStorage.getItem("token");
  if(!token){
    alert("⚠️ You are not logged in!");
    window.location.href = "/frontend/login.html";
    return;
  }
  try{
    const res = await apiFetch("/users/export/csv", {} , true);
    if (!res){
      alert("❌ No response from server");
      return;
    }
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");

    a.href = url ;
    a.download = "users.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    
    alert("✅ Download triggered! Check your Downloads folder.");

  }
  catch(err){
    onsole.error("Error exporting payments:", err);
    alert("❌ Failed to export payments. See console.");
  }
}



// ----------------------
// Expose functions globally
// ----------------------
window.exportusers = exportusers;
// ----------------------
// INIT USERS TABLE ON PAGE LOAD
// ----------------------
document.addEventListener("DOMContentLoaded", fetchUsers);
