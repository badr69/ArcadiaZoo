document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form-review");
    const pseudoInput = document.querySelector("#pseudo");
    const messageInput = document.querySelector("#text-area-review");
    const ratingInput = document.querySelector("#rating");
    const submitBtn = document.querySelector("#submit-btn");
    const reviewsList = document.querySelector("#Reviews-list");

    submitBtn.disabled = true;

    // Validation du formulaire
    function validateForm() {
        submitBtn.disabled = !(pseudoInput.value.trim() && messageInput.value.trim() && ratingInput.value.trim());
    }

    pseudoInput.addEventListener("keyup", validateForm);
    messageInput.addEventListener("keyup", validateForm);
    ratingInput.addEventListener("change", validateForm);

    // Récupération du token CSRF
    const csrfToken = form.querySelector('input[name="csrf_token"]').value;

    // 🔹 Soumission du formulaire
    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        console.log("Submit intercepté !");

        const element_id = form.querySelector('input[name="element_id"]').value;
        const pseudo = pseudoInput.value.trim();
        const message = messageInput.value.trim();
        const rating = ratingInput.value.trim();

        try {
            const response = await fetch("/reviews/add_review", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ pseudo, message, rating, element_id }),
            });

            const data = await response.json();
            console.log("Données envoyées:", { pseudo, message, rating, element_id });
            console.log("Réponse serveur:", data);

            if (response.ok) {
                alert("Votre review a bien été envoyée !");
                form.reset();
                submitBtn.disabled = true;

                // ✅ Ajout direct de la review sans recharger toute la liste
                const newReview = document.createElement("tr");
                newReview.innerHTML = `
                    <td>${data.review_id || ''}</td>
                    <td>${pseudo}</td>
                    <td>${message}</td>
                    <td>${rating}</td>
                    <td>À l'instant</td>
                `;
                reviewsList.prepend(newReview);
            } else {
                alert("Erreur : " + (data.message || "Impossible d’envoyer la review."));
            }
        } catch (err) {
            alert("Erreur lors de l’envoi de la review.");
            console.error(err);
        }
    });

    // 🔹 Chargement initial des reviews
    async function loadReviews() {
        try {
            const response = await fetch("/reviews/get_all_reviews");
            if (!response.ok) throw new Error("Erreur réseau");
            const data = await response.json();

            reviewsList.innerHTML = ""; // Vide la liste

            data.forEach((review) => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${review.id || ''}</td>
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

    // Appel une seule fois
    loadReviews();
});



