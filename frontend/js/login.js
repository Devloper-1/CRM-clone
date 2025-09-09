async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (res.ok) {
    const data = await res.json();
    sessionStorage.setItem("token", data.token);   // store token
    sessionStorage.setItem("userEmail", email);    // optional: store user email
    alert("Login successful!");
    window.location.href = "dashboard.html";       // go to dashboard
  } else {
    const error = await res.json();
    alert("Login failed: " + error.detail);
  }
}
