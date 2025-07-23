document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form-review");
    const pseudoInput = document.querySelector("#pseudo");
    const messageInput = document.querySelector("#text-area-review");
    const ratingInput = document.querySelector("#rating");
    const submitBtn = document.querySelector("#submit-btn");

    submitBtn.disabled = true;

    function validateForm() {
        submitBtn.disabled = !(pseudoInput.value.trim() && messageInput.value.trim() && ratingInput.value.trim());
    }

    pseudoInput.addEventListener("keyup", validateForm);
    messageInput.addEventListener("keyup", validateForm);
    ratingInput.addEventListener("change", validateForm);

    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : '';

    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        console.log("Submit intercepté !");

        const pseudo = pseudoInput.value.trim();
        const message = messageInput.value.trim();
        const rating = ratingInput.value.trim();

        try {
            const response = await fetch("/reviews/submit_review", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ pseudo, message, rating }),
            });

            const data = await response.json();

            console.log("Données envoyées:", { pseudo, message, rating });
            console.log("Réponse serveur:", data);

            if (response.ok) {
                alert("Votre review a bien été envoyée !");
                form.reset();
                submitBtn.disabled = true;

                // Ajout dynamique de la nouvelle review dans la liste
                const reviewsList = document.querySelector("#reviews-list");
                if (reviewsList) {
                    const newReview = document.createElement("div");
                    newReview.classList.add("review-item");
                    newReview.innerHTML = `
                        <strong>${pseudo}</strong> — note : ${rating} <br>
                        <p>${message}</p>
                        <small>À l'instant</small>
                    `;
                    reviewsList.prepend(newReview);
                }

            } else {
                alert("Erreur : " + (data.error || "Impossible d’envoyer la review."));
            }
        } catch (err) {
            alert("Erreur lors de l’envoi de la review.");
            console.error(err);
        }
    });
});
