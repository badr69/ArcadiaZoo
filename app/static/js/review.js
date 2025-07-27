document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form-review");
    const pseudoInput = document.querySelector("#pseudo");
    const messageInput = document.querySelector("#text-area-review");
    const ratingInput = document.querySelector("#rating");
    const submitBtn = document.querySelector("#submit-btn");

    submitBtn.disabled = true;

    // Valide le formulaire en temps réel
    function validateForm() {
        submitBtn.disabled = !(pseudoInput.value.trim() && messageInput.value.trim() && ratingInput.value.trim());
    }

    pseudoInput.addEventListener("keyup", validateForm);
    messageInput.addEventListener("keyup", validateForm);
    ratingInput.addEventListener("change", validateForm);

    // Soumission du formulaire
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const csrfTokenInput = form.querySelector('input[name="csrf_token"]');
        const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

        const pseudo = pseudoInput.value.trim();
        const message = messageInput.value.trim();
        const rating = ratingInput.value.trim();

        try {
            const response = await fetch("/reviews/submit_review", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    ...(csrfToken && { "X-CSRFToken": csrfToken })
                },
                body: JSON.stringify({ pseudo, message, rating }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Votre review a bien été envoyée !");
                form.reset();
                submitBtn.disabled = true;

                // Recharge toute la liste à partir de la base
                await loadReviews();
            } else {
                alert("Erreur : " + (data.error || "Impossible d’envoyer la review."));
            }
        } catch (err) {
            alert("Erreur lors de l’envoi de la review.");
            console.error("Erreur fetch POST :", err);
        }
    });

    // Chargement des avis depuis MongoDB
    async function loadReviews() {
        try {
            const response = await fetch("/reviews/get_all");
            const data = await response.json();

            const reviewsList = document.querySelector("#Reviews-list");
            reviewsList.innerHTML = ""; // Vide la liste existante

            data.forEach((review) => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${review._id}</td>
                    <td>${review.pseudo}</td>
                    <td>${review.message}</td>
                    <td>${review.rating}</td>
                    <td>${review.date ? new Date(review.date).toLocaleString() : ""}</td>
                `;
                reviewsList.appendChild(tr);
            });
        } catch (error) {
            console.error("Erreur lors du chargement des reviews :", error);
        }
    }

    // Appel initial pour afficher les reviews déjà en BDD
    loadReviews();
});
