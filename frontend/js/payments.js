// ================================
// CRM Payment JS — CRUD
// ================================

const API_BASE = "";

// ================================
// Fetch All Payments
// ================================
function fetchPayments() {
  fetch(`${API_BASE}/payments/`)
    .then(res => {
      if (!res.ok) throw new Error("Network error");
      return res.json();
    })
    .then(data => {
      const container = document.getElementById("paymentsTable");
      container.innerHTML = "";

      if (data.length === 0) {
        container.innerHTML = `<tr><td colspan="6" class="text-center py-3">No payments found</td></tr>`;
        return;
      }

      data.forEach(pay => {
        const row = `
          <tr>
            <td>${pay.id}</td>
            <td>${pay.client_id}</td>
            <td>${pay.task_id ?? "N/A"}</td>
            <td>${pay.amount}</td>
            <td>${pay.status}</td>
            <td>${pay.created_at ?? "N/A"}</td>
          </tr>`;
        container.innerHTML += row;
      });
    })
    .catch(err => {
      console.error("Error fetching payments:", err);
      document.getElementById("paymentsTable").innerHTML =
        `<tr><td colspan="6" class="text-center text-red-600">Error loading payments</td></tr>`;
    });
}

// ================================
// Add Payment
// ================================
function addPayment() {
  const paymentData = {
    client_id: document.getElementById("clientId").value,
    task_id: document.getElementById("taskId").value || null,
    amount: parseFloat(document.getElementById("amount").value),
    status: document.getElementById("status").value,
  };

  fetch(`${API_BASE}/payments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paymentData),
  })
    .then(res => res.json())
    .then(() => {
      alert("Payment added successfully!");
      fetchPayments();
    })
    .catch(err => console.error("Error adding payment:", err));
}

// ================================
// Update Payment
// ================================
function updatePayment() {
  const id = document.getElementById("paymentId").value;
  if (!id) return alert("Please enter Payment ID");

  const paymentData = {
    client_id: document.getElementById("clientId").value,
    task_id: document.getElementById("taskId").value || null,
    amount: parseFloat(document.getElementById("amount").value),
    status: document.getElementById("status").value,
  };

  fetch(`${API_BASE}/payments/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(paymentData),
  })
    .then(res => res.json())
    .then(() => {
      alert("Payment updated successfully!");
      fetchPayments();
    })
    .catch(err => console.error("Error updating payment:", err));
}

// ================================
// Delete Payment
// ================================
function deletePayment() {
  const id = document.getElementById("paymentId").value;
  if (!id) return alert("Please enter Payment ID");

  fetch(`${API_BASE}/payments/${id}`, { method: "DELETE" })
    .then(() => {
      alert("Payment deleted successfully!");
      fetchPayments();
    })
    .catch(err => console.error("Error deleting payment:", err));
}

window.fetchPayments = fetchPayments;
document.addEventListener("DOMContentLoaded", fetchPayments);
