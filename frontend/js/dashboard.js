// ============================================================
// Dashboard JS — Sidebar, Logout, Chart
// ============================================================

// 1️⃣ Check login
const token = sessionStorage.getItem("token");
if (!token) window.location.href = "/frontend/login.html";

// 2️⃣ Sidebar toggle
const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("menu-toggle");
const overlay = document.getElementById("overlay");

toggleBtn?.addEventListener("click", () => {
  sidebar.classList.toggle("-translate-x-full");
  overlay.classList.toggle("hidden");
});

overlay?.addEventListener("click", () => {
  sidebar.classList.add("-translate-x-full");
  overlay.classList.add("hidden");
});

// 3️⃣ Logout function
function logout() {
  sessionStorage.clear();
  window.location.href = "/frontend/login.html";
}

document.getElementById("logoutBtnTop")?.addEventListener("click", logout);
document.getElementById("logoutBtnSidebar")?.addEventListener("click", logout);

// 4️⃣ Load chart
async function loadChartData() {
  const headers = { "Authorization": `Bearer ${token}` };

  try {
    const [clientsRes, usersRes, tasksRes, paymentsRes] = await Promise.all([
      fetch("http://127.0.0.1:8000/clients/", { headers }),
      fetch("http://127.0.0.1:8000/users/", { headers }),
      fetch("http://127.0.0.1:8000/tasks/", { headers }),
      fetch("http://127.0.0.1:8000/payments/", { headers }),
    ]);

    const [clients, users, tasks, payments] = await Promise.all([
      clientsRes.ok ? clientsRes.json() : [],
      usersRes.ok ? usersRes.json() : [],
      tasksRes.ok ? tasksRes.json() : [],
      paymentsRes.ok ? paymentsRes.json() : [],
    ]);

    const counts = [clients.length, users.length, tasks.length, payments.length];

    const canvas = document.getElementById("clientsChart");
    const ctx = canvas.getContext("2d");
    canvas.height = 300;

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Clients", "Users", "Tasks", "Payments"],
        datasets: [{
          label: "Counts",
          data: counts,
          backgroundColor: ["#1abc9c", "#3498db", "#f1c40f", "#e74c3c"]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
      }
    });

  } catch (err) {
    console.error("Error loading chart data:", err);
  }
}

// Run chart
loadChartData();
