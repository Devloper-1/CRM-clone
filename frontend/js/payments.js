// ============================================================
// File: frontend/js/payments.js
// Description: API CRUD operations for Payments (JWT protected)
// ============================================================

// ----------------------
// PAYMENT FETCH ALL
// ----------------------
async function fetchPayments() {
  try {
    const data = await apiFetch("/payments/");
    const container = document.getElementById("paymentsTable");
    if (!container) return console.error("❌ paymentsTable element not found");

    container.innerHTML = "";

    if (!data || data.length === 0) {
      container.innerHTML = `<tr><td colspan="6" class="text-center py-3">No payments found</td></tr>`;
      return;
    }

    data.forEach(pay => {
      const task = pay.task_id ?? "N/A";
      const created = pay.created_at ?? "N/A";

      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="border px-4 py-2">${pay.id}</td>
        <td class="border px-4 py-2">${pay.client_id}</td>
        <td class="border px-4 py-2">${task}</td>
        <td class="border px-4 py-2">${pay.amount}</td>
        <td class="border px-4 py-2">${pay.status}</td>
        <td class="border px-4 py-2">${created}</td>
      `;
      container.appendChild(row);
    });
  } catch (err) {
    console.error("Error fetching payments:", err);
    document.getElementById(
      "paymentsTable"
    ).innerHTML = `<tr><td colspan="6" class="text-center text-red-600">Error loading payments</td></tr>`;
  }
}

// ----------------------
// PAYMENT ADD
// ----------------------
async function addPayment() {
  const paymentData = {
    client_id: document.getElementById("clientId").value,
    task_id: document.getElementById("taskId").value || null,
    amount: parseFloat(document.getElementById("amount").value),
    status: document.getElementById("status").value,
  };

  try {
    await apiFetch("/payments", { method: "POST", body: JSON.stringify(paymentData) });
    alert("Payment added successfully!");
    fetchPayments();
  } catch (err) {
    console.error("Error adding payment:", err);
    alert("Error adding payment");
  }
}

// ----------------------
// PAYMENT UPDATE
// ----------------------
async function updatePayment() {
  const id = document.getElementById("paymentId").value;
  if (!id) return alert("Please enter Payment ID");

  const paymentData = {
    client_id: document.getElementById("clientId").value,
    task_id: document.getElementById("taskId").value || null,
    amount: parseFloat(document.getElementById("amount").value),
    status: document.getElementById("status").value,
  };

  try {
    await apiFetch(`/payments/${id}`, { method: "PUT", body: JSON.stringify(paymentData) });
    alert("Payment updated successfully!");
    fetchPayments();
  } catch (err) {
    console.error("Error updating payment:", err);
    alert("Error updating payment");
  }
}

// ----------------------
// PAYMENT DELETE
// ----------------------
async function deletePayment() {
  const id = document.getElementById("paymentId").value;
  if (!id) return alert("Please enter Payment ID");

  try {
    await apiFetch(`/payments/${id}`, { method: "DELETE" });
    alert("Payment deleted successfully!");
    fetchPayments();
  } catch (err) {
    console.error("Error deleting payment:", err);
    alert("Error deleting payment");
  }
}

// ----------------------
// Expose functions globally
// ----------------------
window.fetchPayments = fetchPayments;
window.addPayment = addPayment;
window.updatePayment = updatePayment;
window.deletePayment = deletePayment;

// ----------------------
// Load payments on page load
// ----------------------
document.addEventListener("DOMContentLoaded", fetchPayments);
