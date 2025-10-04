// ============================================================
// File: frontend/js/tasks.js
// Description: API CRUD operations for Tasks (JWT protected)
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

  // ----------------------
  // TASK FETCH ALL
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
      document.getElementById(
        "tasksTable"
      ).innerHTML = `<tr><td colspan="4" class="text-center text-red-600">Error loading tasks</td></tr>`;
    }
  }

  // ----------------------
  // TASK ADD
  // ----------------------
  async function addTask() {
    const taskData = {
      client_id: document.getElementById("clientId").value,
      description: document.getElementById("description").value,
      status: document.getElementById("status").value,
    };

    try {
      await apiFetch("/tasks", { method: "POST", body: JSON.stringify(taskData) });
      alert("Task added successfully!");
      fetchTasks();
    } catch (err) {
      console.error("Error adding task:", err);
      alert("Error adding task");
    }
  }

  // ----------------------
  // TASK UPDATE
  // ----------------------
  async function updateTask() {
    const id = document.getElementById("taskId").value;
    if (!id) return alert("Please enter Task ID");

    const taskData = {
      client_id: document.getElementById("clientId").value,
      description: document.getElementById("description").value,
      status: document.getElementById("status").value,
    };

    try {
      await apiFetch(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(taskData) });
      alert("Task updated successfully!");
      fetchTasks();
    } catch (err) {
      console.error("Error updating task:", err);
      alert("Error updating task");
    }
  }

  // ----------------------
  // TASK DELETE
  // ----------------------
  async function deleteTask() {
    const id = document.getElementById("taskId").value;
    if (!id) return alert("Please enter Task ID");

    try {
      await apiFetch(`/tasks/${id}`, { method: "DELETE" });
      alert("Task deleted successfully!");
      fetchTasks();
    } catch (err) {
      console.error("Error deleting task:", err);
      alert("Error deleting task");
    }
  }

  // ----------------------
  // Expose functions globally
  // ----------------------
  window.fetchTasks = fetchTasks;
  window.addTask = addTask;
  window.updateTask = updateTask;
  window.deleteTask = deleteTask;

  // ----------------------
  // Load tasks initially
  // ----------------------
  fetchTasks();

  // ----------------------
  // Export Tasks to CSV
  // ----------------------
  const exportBtn = document.getElementById("exportTasksBtn");
  if (exportBtn) {
    exportBtn.addEventListener("click", async () => {
      const token = sessionStorage.getItem("token");
      if (!token) {
        window.location.href = "/frontend/login.html";
        return;
      }

      try {
        const res = await apiFetch("/tasks/export/csv", {}, true);
        if (!res) return;

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "tasks.csv";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

      } catch (err) {
        console.error("Error exporting tasks:", err);
        alert("Failed to export tasks");
      }
    });
  }

});
