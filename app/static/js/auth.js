console.log("auth.js loaded");

/* ---------------- REGISTER ---------------- */
function register() {
  fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("name")?.value,
      email: document.getElementById("email")?.value,
      password: document.getElementById("password")?.value
    })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("msg").innerText = data.message;
      if (data.message.toLowerCase().includes("success")) {
        window.location.href = "/login";
      }
    });
}

/* ---------------- LOGIN ---------------- */
const loginForm = document.getElementById("loginForm");

if (!loginForm) {
  console.error("❌ loginForm not found");
} else {
  console.log("✅ loginForm found");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log("🔐 Sending login request");

    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    console.log("🔥 Login response:", data);

    if (res.ok) {
      // ✅ THIS IS THE CRITICAL LINE
      localStorage.setItem("user", JSON.stringify(data.user));
      console.log("✅ User stored in localStorage");

      window.location.href = "/dashboard";
    } else {
      document.getElementById("message").innerText = data.message;
    }
  });
}
