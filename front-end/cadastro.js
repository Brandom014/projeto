const API = "http://127.0.0.1:8000";

const form = document.getElementById("cadastroForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const usuario = document.getElementById("usuario").value;
  const email = document.getElementById("email").value;
  const senha = document.getElementById("senha").value;
  const confirmar = document.getElementById("confirmar").value;

  if (senha !== confirmar) {
    alert("As senhas não coincidem");
    return;
  }

  try {
    const res = await fetch(`${API}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        nome: usuario,
        email: email,
        senha: senha
      })
    });

    const data = await res.json();

    console.log(data);

    if (res.ok) {
      alert("Cadastro feito!");
      window.location.href = "login.html";
    } else {
      alert(data.erro || "Erro ao cadastrar");
    }

  } catch (err) {
    console.error(err);
    alert("Erro ao conectar com o servidor");
  }
});