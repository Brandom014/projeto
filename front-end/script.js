const API = "http://127.0.0.1:8000";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("usuario").value;
  const senha = document.getElementById("senha").value;

  try {
    const response = await fetch(`${API}/login`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ email, senha })
    });

    const data = await response.json();

    console.log("LOGIN:", data);

    if (response.ok && !data.erro) {
      alert("Login realizado!");
      window.location.href = "dashboard.html";
    } else {
      alert(data.erro || "Erro no login");
    }

  } catch (err) {
    console.error(err);
    alert("Erro ao conectar com o servidor");
  }
});