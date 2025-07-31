document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("#form-review");
    const submitBtn = document.querySelector("#submit-btn");
    const pseudoInput = document.querySelector("#pseudo");
    const messageInput = document.querySelector("#text-area-review");
    const ratingInput = document.querySelector("#rating");
    const reviewsList = document.querySelector("#Reviews-list");

    if (!form || !submitBtn || !pseudoInput || !messageInput || !ratingInput || !reviewsList) {
        // Certains éléments ne sont pas présents, on arrête le script.
        return;
    }

    submitBtn.disabled = true;

    // Fonction de validation simple
    function validateForm() {
        const isValid =
            pseudoInput.value.trim() !== "" &&
            messageInput.value.trim() !== "" &&
            ratingInput.value.trim() !== "";
        submitBtn.disabled = !isValid;
    }

    // Valider à chaque saisie / changement
    pseudoInput.addEventListener("input", validateForm);
    messageInput.addEventListener("input", validateForm);
    ratingInput.addEventListener("change", validateForm);

    // Récupération du token CSRF depuis la meta dans base.html
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const element_id = form.querySelector('input[name="element_id"]').value;

        try {
            const response = await fetch("/reviews/add_review", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    pseudo: pseudoInput.value.trim(),
                    message: messageInput.value.trim(),
                    rating: ratingInput.value.trim(),
                    element_id: element_id
                }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("✅ Votre review a bien été envoyée !");
                form.reset();
                submitBtn.disabled = true;
                loadReviews(); // recharge la liste
            } else {
                alert("❌ Erreur : " + (data.message || "Impossible d’envoyer la review."));
            }
        } catch (err) {
            alert("❌ Erreur lors de l’envoi de la review.");
            console.error(err);
        }
    });

    async function loadReviews() {
        try {
            const response = await fetch("/reviews/published");
            if (!response.ok) throw new Error("Erreur réseau lors du chargement des reviews");

            const reviews = await response.json();

            if (!Array.isArray(reviews) || reviews.length === 0) {
                reviewsList.innerHTML = `<tr><td colspan="4" class="text-center">Aucune review publiée pour le moment.</td></tr>`;
                return;
            }

            let html = "";
            reviews.forEach(r => {
                html += `<tr>
                    <td>${escapeHtml(r.pseudo)}</td>
                    <td>${escapeHtml(r.message)}</td>
                    <td>${escapeHtml(r.rating)}</td>
                    <td>${r.created_at ? new Date(r.created_at).toLocaleString() : ''}</td>
                </tr>`;
            });

            reviewsList.innerHTML = html;

        } catch (err) {
            reviewsList.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Erreur lors du chargement des reviews.</td></tr>`;
            console.error(err);
        }
    }

    // Simple fonction d'échappement HTML pour éviter injection
    function escapeHtml(text) {
    if (typeof text !== "string") {
        text = String(text ?? ""); // convertit null/undefined/number → string
    }
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

    // Chargement initial des reviews
    loadReviews();
});


