// Attendre que le DOM soit chargé
document.addEventListener("DOMContentLoaded", () => {

  const form = document.querySelector("#loginForm"); // Formulaire
  const messageBox = document.querySelector("#message-box"); // Div pour messages
  const submitButton = form.querySelector('button[type="submit"]'); // Bouton submit

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Empêche le rechargement de la page

    // Réinitialiser le message
    messageBox.textContent = "";
    messageBox.className = "";

    // Préparer les données du formulaire
    const formData = new FormData(form);

    // Conversion sécurisée : forcer toutes les valeurs en string
    const data = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
      data.append(key, value.toString());
    }

    // Désactiver le bouton pendant la requête
    submitButton.disabled = true;
    submitButton.textContent = "Connexion...";

    try {
      // Requête POST vers le backend Flask
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest", // Indique AJAX
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: data.toString() // Envoi des données encodées
      });

      const result = await response.json(); // JSON renvoyé par le backend

      if (result.success) {
        // Login réussi → redirection selon rôle
        window.location.href = result.redirect;
      } else {
        // Affichage des erreurs
        if (result.message) {
          messageBox.textContent = result.message;
          messageBox.className = "alert alert-danger";
        } else if (result.errors) {
          let errorsHtml = "<ul>";
          for (const field in result.errors) {
            result.errors[field].forEach(error => {
              errorsHtml += `<li><strong>${field}</strong>: ${error}</li>`;
            });
          }
          errorsHtml += "</ul>";
          messageBox.innerHTML = errorsHtml;
          messageBox.className = "alert alert-danger";

          // Focus sur le premier champ en erreur
          const firstField = Object.keys(result.errors)[0];
          form.querySelector(`[name="${firstField}"]`).focus();
        }

        // Supprimer automatiquement le message après 5 secondes
        setTimeout(() => {
          messageBox.textContent = "";
          messageBox.className = "";
        }, 5000);
      }

    } catch (error) {
      // Erreur serveur
      messageBox.textContent = "Erreur serveur. Merci de réessayer plus tard.";
      messageBox.className = "alert alert-danger";
      console.error("Fetch error:", error);
    } finally {
      // Réactiver le bouton submit
      submitButton.disabled = false;
      submitButton.textContent = "Se connecter";
    }

  });
});
