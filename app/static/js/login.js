document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Rediriger vers le dashboard correspondant
                window.location.href = data.redirect;
            } else {
                // Afficher les erreurs
                const alertBox = document.createElement("div");
                alertBox.className = "alert alert-danger";
                alertBox.innerText = data.message || "Erreur inconnue";

                // Insère au-dessus du formulaire
                form.prepend(alertBox);
            }
        } catch (err) {
            console.error("Erreur fetch:", err);
            alert("Erreur réseau. Veuillez réessayer.");
        }
    });
});
