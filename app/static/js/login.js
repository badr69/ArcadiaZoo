console.log("login.js chargé");

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#loginForm");
  const messageBox = document.querySelector("#message-box");
  const submitButton = form.querySelector("#submit-btn");

  console.log("Form trouvé :", form);
  console.log("Message box trouvé :", messageBox);
  console.log("Bouton submit trouvé :", submitButton);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Submit déclenché");

    // Réinitialiser le message
    messageBox.textContent = "";
    messageBox.className = "";

    // Préparer les données du formulaire
    const formData = new FormData(form);
    const data = new URLSearchParams();
    for (const [key, value] of formData.entries()) {
      data.append(key, value.toString());
    }

    // Récupérer le CSRF token
    const csrfToken = form.querySelector('input[name="csrf_token"]').value;

    console.log("Envoi du fetch vers :", form.action);
    console.log("Données envoyées :", Object.fromEntries(data.entries()));

    // Désactiver le bouton
    submitButton.disabled = true;
    submitButton.value = "Connexion...";

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        body: data.toString()
      });

      console.log("Réponse reçue :", response);

      const result = await response.json();
      console.log("JSON reçu :", result);

      if (result.success) {
        console.log("Login réussi ! Redirection vers :", result.redirect);
            setTimeout(() => {
        window.location.href = result.redirect;
        }, 2000); // attend 2 secondes avant de rediriger
       
      } else {
        console.log("Erreur login :", result);
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

          const firstField = Object.keys(result.errors)[0];
          form.querySelector(`[name="${firstField}"]`).focus();
        }

        // Supprimer le message après 5 secondes
        setTimeout(() => {
          messageBox.textContent = "";
          messageBox.className = "";
        }, 5000);
      }

    } catch (error) {
      messageBox.textContent = "Erreur serveur. Merci de réessayer plus tard.";
      messageBox.className = "alert alert-danger";
      console.error("Fetch error:", error);
    } finally {
      submitButton.disabled = false;
      submitButton.value = "Se connecter";
    }
  });
});



// console.log("login.js chargé");
//
// document.addEventListener("DOMContentLoaded", () => {
//
//   const form = document.querySelector("#loginForm"); // Formulaire
//   const messageBox = document.querySelector("#message-box"); // Div pour messages
//   const submitButton = form.querySelector("#submit-btn"); // Bouton submit
//
//   console.log("Form trouvé :", form);
//   console.log("Message box trouvé :", messageBox);
//   console.log("Bouton submit trouvé :", submitButton);
//
//   form.addEventListener("submit", async (e) => {
//     e.preventDefault(); // Empêche le rechargement de la page
//     console.log("Submit déclenché");
//
//     // Réinitialiser le message
//     messageBox.textContent = "";
//     messageBox.className = "";
//
//     // Préparer les données du formulaire
//     const formData = new FormData(form);
//     const data = new URLSearchParams();
//     for (const [key, value] of formData.entries()) {
//       data.append(key, value.toString());
//     }
//
//     console.log("Envoi du fetch vers :", form.action);
//     console.log("Données envoyées :", Object.fromEntries(data));
//
//     // Désactiver le bouton pendant la requête
//     submitButton.disabled = true;
//     submitButton.value = "Connexion...";
//
//     try {
//       const response = await fetch(form.action, {
//         method: "POST",
//         headers: {
//           "X-Requested-With": "XMLHttpRequest",
//           "Content-Type": "application/x-www-form-urlencoded",
//         },
//         body: data.toString()
//       });
//
//       console.log("Réponse reçue :", response);
//
//       const result = await response.json();
//       console.log("JSON reçu :", result);
//
//       if (result.success) {
//         console.log("Login réussi ! Redirection vers :", result.redirect);
//         // window.location.href = result.redirect; // <- commenter pour debug
//       } else {
//         console.log("Erreur login :", result);
//         if (result.message) {
//           messageBox.textContent = result.message;
//           messageBox.className = "alert alert-danger";
//         } else if (result.errors) {
//           let errorsHtml = "<ul>";
//           for (const field in result.errors) {
//             result.errors[field].forEach(error => {
//               errorsHtml += `<li><strong>${field}</strong>: ${error}</li>`;
//             });
//           }
//           errorsHtml += "</ul>";
//           messageBox.innerHTML = errorsHtml;
//           messageBox.className = "alert alert-danger";
//
//           const firstField = Object.keys(result.errors)[0];
//           form.querySelector(`[name="${firstField}"]`).focus();
//         }
//       }
//
//     } catch (error) {
//       messageBox.textContent = "Erreur serveur. Merci de réessayer plus tard.";
//       messageBox.className = "alert alert-danger";
//       console.error("Fetch error:", error);
//     } finally {
//       submitButton.disabled = false;
//       submitButton.value = "Se connecter";
//     }
//
//   });
//
// });
//
//
//
