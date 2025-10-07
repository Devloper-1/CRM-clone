// ============================================================
// File: frontend/js/tasks.js
// Description: API CRUD operations for Tasks (JWT protected)
// ============================================================

// ----------------------
// FETCH ALL TASKS
// ----------------------
async function fetchTasks() {
  try {
    const data = await apiFetch("/tasks/");
    const container = document.getElementById("tasksTable");
    if (!container) return console.error("❌ tasksTable element not found");

    container.innerHTML = "";

    if (!data || data.length === 0) {
      container.innerHTML = `<tr><td colspan="4" class="text-center py-3">No tasks found</td></tr>`;
      return;
    }

    data.forEach(task => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="border px-4 py-2">${task.id}</td>
        <td class="border px-4 py-2">${task.client_id}</td>
        <td class="border px-4 py-2">${task.description}</td>
        <td class="border px-4 py-2">${task.status}</td>
      `;
      container.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching tasks:", err);
    const container = document.getElementById("tasksTable");
    if (container) {
      container.innerHTML = `<tr><td colspan="4" class="text-center text-red-600">Error loading tasks</td></tr>`;
    }
  }
}

// ----------------------
// ADD TASK
// ----------------------
async function addTask() {
  const taskData = {
    client_id: document.getElementById("clientId").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value,
  };

  try {
    await apiFetch("/tasks", { method: "POST", body: JSON.stringify(taskData) });
    alert("✅ Task added successfully!");
    fetchTasks();
  } catch (err) {
    console.error("Error adding task:", err);
    alert("❌ Error adding task");
  }
}

// ----------------------
// UPDATE TASK
// ----------------------
async function updateTask() {
  const id = document.getElementById("taskId").value;
  if (!id) return alert("⚠️ Please enter Task ID");

  const taskData = {
    client_id: document.getElementById("clientId").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value,
  };

  try {
    await apiFetch(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(taskData) });
    alert("✅ Task updated successfully!");
    fetchTasks();
  } catch (err) {
    console.error("Error updating task:", err);
    alert("❌ Error updating task");
  }
}

// ----------------------
// DELETE TASK
// ----------------------
async function deleteTask() {
  const id = document.getElementById("taskId").value;
  if (!id) return alert("⚠️ Please enter Task ID");

  try {
    await apiFetch(`/tasks/${id}`, { method: "DELETE" });
    alert("✅ Task deleted successfully!");
    fetchTasks();
  } catch (err) {
    console.error("Error deleting task:", err);
    alert("❌ Error deleting task");
  }
}

// ----------------------
// EXPORT TASKS TO CSV
// ----------------------
async function exportTasks() {
  alert("✅ Export button clicked!"); // Debug alert

  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("⚠️ You are not logged in!");
    window.location.href = "/frontend/login.html";
    return;
  }

  try {
    const res = await apiFetch("/tasks/export/csv", {}, true);
    if (!res) {
      alert("❌ No response from server");
      return;
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "tasks.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    alert("✅ Download triggered! Check your Downloads folder.");
  } catch (err) {
    console.error("Error exporting tasks:", err);
    alert("❌ Failed to export tasks. See console.");
  }
}

// ----------------------
// GLOBAL EXPOSE
// ----------------------
window.fetchTasks = fetchTasks;
window.addTask = addTask;
window.updateTask = updateTask;
window.deleteTask = deleteTask;
window.exportTasks = exportTasks;

// ----------------------
// LOAD TASKS ON PAGE LOAD
// ----------------------
document.addEventListener("DOMContentLoaded", fetchTasks);
