// Récupération sécurisée du token CSRF
const csrfMeta = document.querySelector('meta[name="csrf-token"]');
const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : null;
if (!csrfToken) {
    console.warn("⚠️ Token CSRF introuvable !");
} else {
    console.log("CSRF Token détecté :", csrfToken);
}

document.addEventListener("DOMContentLoaded", () => {
    try {
        const reviewsList = document.querySelector("#Employee-Reviews-list");
        if (!reviewsList) {
            console.warn("Element #Employee-Reviews-list introuvable, arrêt du script.");
            return;
        }
        console.log("reviewsList trouvé :", reviewsList);

        // Fonction d'échappement HTML pour éviter injection XSS
        function escapeHtml(text) {
            if (typeof text !== "string") {
                text = String(text ?? "");
            }
            return text.replace(/[&<>"']/g, (m) => {
                switch (m) {
                    case '&': return "&amp;";
                    case '<': return "&lt;";
                    case '>': return "&gt;";
                    case '"': return "&quot;";
                    case "'": return "&#039;";
                    default: return m;
                }
            });
        }

        // Chargement et affichage des reviews
        async function loadReviews() {
            try {
                const response = await fetch("/reviews/get_all_reviews");
                if (!response.ok) throw new Error("Erreur réseau lors du chargement des reviews");

                const data = await response.json();

                reviewsList.innerHTML = "";

                data.forEach((review) => {
                    const tr = document.createElement("tr");
                    tr.innerHTML = `
                        <td>${escapeHtml(review.id ?? "")}</td>
                        <td>${escapeHtml(review.pseudo)}</td>
                        <td>${escapeHtml(review.message)}</td>
                        <td>${escapeHtml(review.rating)}</td>
                        <td>${review.date ? new Date(review.date).toLocaleString() : ""}</td>
                        <td>
                            <div class="btn-group" role="group" aria-label="Actions">
                                <button class="btn-publish btn btn-primary btn-sm me-2" data-id="${escapeHtml(review.id)}"
                                    ${review.published ? "disabled" : ""}>
                                    ${review.published ? "Publié" : "Publier"}
                                </button>
                                <button class="btn-delete btn btn-danger btn-sm me-2" data-id="${escapeHtml(review.id)}">Delete</button>
                            </div>
                        </td>
                    `;
                    reviewsList.appendChild(tr);
                });
            } catch (error) {
                console.error("Erreur lors du chargement des reviews :", error);
                reviewsList.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Erreur lors du chargement des reviews.</td></tr>`;
            }
        }

        // Gestion des clics sur Publish/Delete
        reviewsList.addEventListener("click", async (event) => {
            const target = event.target;
            const id = target.getAttribute("data-id");
            if (!id) return;

            // Publication
            if (target.classList.contains("btn-publish")) {
                if (!confirm("Publier cette review ?")) return;

                try {
                    const response = await fetch(`/reviews/publish/${id}`, {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json",
                            ...(csrfToken ? { "X-CSRFToken": csrfToken } : {})
                        },
                    });

                    if (response.ok) {
                        alert("✅ Review publiée !");
                        target.textContent = "Publié";
                        target.disabled = true;
                    } else {
                        alert("❌ Erreur lors de la publication.");
                    }
                } catch (error) {
                    alert("❌ Erreur réseau lors de la publication.");
                    console.error(error);
                }
            }

            // Suppression
            if (target.classList.contains("btn-delete")) {
                if (!confirm("Supprimer cette review ?")) return;

                try {
                    const response = await fetch(`/reviews/delete/${id}`, {
                        method: "DELETE",
                        headers: {
                            "Content-Type": "application/json",
                            ...(csrfToken ? { "X-CSRFToken": csrfToken } : {})
                        },
                    });

                    if (response.ok) {
                        alert("✅ Review supprimée !");
                        await loadReviews();
                    } else {
                        alert("❌ Erreur lors de la suppression.");
                    }
                } catch (error) {
                    alert("❌ Erreur réseau lors de la suppression.");
                    console.error(error);
                }
            }
        });

        // Chargement initial
        loadReviews();

    } catch (error) {
        console.error("Erreur inattendue au chargement du DOM :", error);
    }
});

