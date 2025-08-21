document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:8000/clients")
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      const container = document.getElementById("clientsTable");
      container.innerHTML = ""; // clear "Loading..."
      
      if (data.length === 0) {
        container.innerHTML = `<tr><td colspan="3">No clients found</td></tr>`;
        return;
      }

      data.forEach(client => {
        let row = `
          <tr>
            <td>${client.id}</td>
            <td>${client.name}</td>
            <td>${client.email}</td>
          </tr>`;
        container.innerHTML += row;
      });
    })
    .catch(error => {
      console.error("Error fetching clients:", error);
      document.getElementById("clientsTable").innerHTML =
        `<tr><td colspan="3">Error loading clients</td></tr>`;
    });
});
