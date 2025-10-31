document.addEventListener("DOMContentLoaded", () => {
  // === Inscription ===
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = {
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      };

      const res = await fetch("/users/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const msg = document.getElementById("message");
      if (res.ok) {
        const json = await res.json();
        msg.textContent = `✅ Compte créé avec succès (ID: ${json.user_id})`;
        msg.style.color = "green";
      } else {
        const err = await res.json();
        msg.textContent = `❌ Erreur : ${err.detail}`;
        msg.style.color = "red";
      }
    });
  }

  // === Connexion ===
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;

      const params = new URLSearchParams({ email, password });
      const res = await fetch(`/auth/login?${params.toString()}`, { method: "POST" });

      const msg = document.getElementById("loginMessage");
      if (res.ok) {
        const json = await res.json();
        localStorage.setItem("token", json.access_token);
        msg.textContent = `✅ Bienvenue ${json.username} !`;
        msg.style.color = "green";
      } else {
        const err = await res.json();
        msg.textContent = `❌ Erreur : ${err.detail}`;
        msg.style.color = "red";
      }
    });
  }
});
