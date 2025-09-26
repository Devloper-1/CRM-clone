// ================================
// CRM Task JS — CRUD
// ================================


// ================================
// Fetch All Tasks
// ================================
function fetchTasks() {
  apiFetch(`${API_BASE}/tasks/`)
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.json();
    })
    .then(data => {
      const container = document.getElementById("tasksTable");
      container.innerHTML = "";

      if (data.length === 0) {
        container.innerHTML = `<tr><td colspan="4" class="text-center py-3">No tasks found</td></tr>`;
        return;
      }

      data.forEach(task => {
        const row = `
          <tr>
            <td>${task.id}</td>
            <td>${task.client_id}</td>
            <td>${task.description}</td>
            <td>${task.status}</td>
          </tr>`;
        container.innerHTML += row;
      });
    })
    .catch(err => {
      console.error("Error fetching tasks:", err);
      document.getElementById("tasksTable").innerHTML =
        `<tr><td colspan="4" class="text-center text-red-600">Error loading tasks</td></tr>`;
    });
}

// ================================
// Add New Task
// ================================
function addTask() {
  const taskData = {
    client_id: document.getElementById("clientId").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value,
  };

  apiFetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(taskData),
  })
    .then(res => res.json())
    .then(() => {
      alert("Task added successfully!");
      fetchTasks();
    })
    .catch(err => console.error("Error adding task:", err));
}

// ================================
// Update Task
// ================================
function updateTask() {
  const id = document.getElementById("taskId").value;
  if (!id) return alert("Please enter Task ID");

  const taskData = {
    client_id: document.getElementById("clientId").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value,
  };

  apiFetch(`${API_BASE}/tasks/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(taskData),
  })
    .then(res => res.json())
    .then(() => {
      alert("Task updated successfully!");
      fetchTasks();
    })
    .catch(err => console.error("Error updating task:", err));
}

// ================================
// Delete Task
// ================================
function deleteTask() {
  const id = document.getElementById("taskId").value;
  if (!id) return alert("Please enter Task ID");

  fetch(`${API_BASE}/tasks/${id}`, { method: "DELETE" })
    .then(() => {
      alert("Task deleted successfully!");
      fetchTasks();
    })
    .catch(err => console.error("Error deleting task:", err));
}

window.fetchTasks = fetchTasks;
document.addEventListener("DOMContentLoaded", fetchTasks);
