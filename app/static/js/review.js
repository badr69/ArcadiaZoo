document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form-review");
    const pseudoInput = document.querySelector("#pseudo");
    const messageInput = document.querySelector("#text-area-review");
    const ratingInput = document.querySelector("#rating");
    const submitBtn = document.querySelector("#submit-btn");
    const reviewsList = document.querySelector("#Reviews-list"); // si présent ici

    if (!form || !submitBtn) return; // stop si on est pas sur la bonne page

    submitBtn.disabled = true;

    function validateForm() {
        submitBtn.disabled = !(pseudoInput.value.trim() && messageInput.value.trim() && ratingInput.value.trim());
    }

    pseudoInput.addEventListener("keyup", validateForm);
    messageInput.addEventListener("keyup", validateForm);
    ratingInput.addEventListener("change", validateForm);

    const csrfToken = form.querySelector('input[name="csrf_token"]').value;

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

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

            if (response.ok) {
                alert("✅ Votre review a bien été envoyée !");
                form.reset();
                submitBtn.disabled = true;

                // Optionnel : ajouter la review dans la liste si elle est affichée ici
                if (reviewsList) {
                    const newReview = document.createElement("tr");
                    newReview.innerHTML = `
                        <td>${data.review_id || ''}</td>
                        <td>${pseudo}</td>
                        <td>${message}</td>
                        <td>${rating}</td>
                        <td>À l'instant</td>
                        <td>
                          <div class="btn-group" role="group" aria-label="Actions">
                            <button class="btn-delete btn btn-danger btn-sm me-2" data-id="${data.review_id}">Delete</button>
                            <button class="btn-publish btn btn-primary btn-sm me-2" data-id="${data.review_id}">Publish</button>
                          </div>
                        </td>
                    `;
                    reviewsList.prepend(newReview);
                }
            } else {
                alert("❌ Erreur : " + (data.message || "Impossible d’envoyer la review."));
            }
        } catch (err) {
            alert("❌ Erreur lors de l’envoi de la review.");
            console.error(err);
        }
    });
});




