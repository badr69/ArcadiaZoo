document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#login-form");
  const messageBox = document.querySelector("#message-box");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Reset message box
    messageBox.innerHTML = "";
    messageBox.className = "";

    const formData = new FormData(form);
    const data = new URLSearchParams(formData);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: data.toString(),
      });

      const result = await response.json();

      if (result.success) {
        // Redirection vers l'URL reçue
        window.location.href = result.redirect;
      } else {
        // Afficher le message d'erreur
        if (result.message) {
          messageBox.textContent = result.message;
          messageBox.className = "alert alert-danger";
        } else if (result.errors) {
          // Afficher les erreurs de validation formulaire
          let errorsHtml = "<ul>";
          for (const field in result.errors) {
            result.errors[field].forEach((error) => {
              errorsHtml += `<li><strong>${field}</strong>: ${error}</li>`;
            });
          }
          errorsHtml += "</ul>";
          messageBox.innerHTML = errorsHtml;
          messageBox.className = "alert alert-danger";
        }
      }
    } catch (error) {
      messageBox.textContent = "Erreur serveur. Merci de réessayer plus tard.";
      messageBox.className = "alert alert-danger";
      console.error("Fetch error:", error);
    }
  });
});
