const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
console.log("CSRF Token détecté :", csrfToken);

// --- Exécution après chargement du DOM ---
document.addEventListener("DOMContentLoaded", () => {

    const reviewsList = document.querySelector("#Employee-Reviews-list");
    console.log("reviewsList trouvé :", reviewsList);
    if (!reviewsList) return;

    // --- Fonction pour charger les reviews ---
    async function loadReviews() {
        try {
            const response = await fetch("/reviews/get_all_reviews");
            if (!response.ok) throw new Error("Erreur réseau");
            const data = await response.json();

            reviewsList.innerHTML = "";

            data.forEach((review) => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${review.id || ''}</td>
                    <td>${review.pseudo}</td>
                    <td>${review.message}</td>
                    <td>${review.rating}</td>
                    <td>${review.date ? new Date(review.date).toLocaleString() : ""}</td>
                    <td>
                      <div class="btn-group" role="group" aria-label="Actions">
                        <button class="btn-publish btn btn-primary btn-sm me-2" data-id="${review.id}" 
                            ${review.published ? "disabled" : ""}>
                            ${review.published ? "Publié" : "Publier"}
                        </button>
                        <button class="btn-delete btn btn-danger btn-sm me-2" data-id="${review.id}">Delete</button>
                      </div>
                    </td>
                `;
                reviewsList.appendChild(tr);
            });
        } catch (error) {
            console.error("Erreur lors du chargement des reviews :", error);
        }
    }

    // --- Gestion des clics sur les boutons Delete et Publish ---
    reviewsList.addEventListener("click", async (event) => {
        const target = event.target;
        const id = target.getAttribute("data-id");
        if (!id) return;

        // --- Publication d'une review ---
        if (target.classList.contains("btn-publish")) {
            if (confirm("Publier cette review ?")) {
                try {
                    const response = await fetch(`/reviews/publish/${id}`, {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken,
                        },
                    });

                    if (response.ok) {
                        alert("✅ Review publiée !");
                        // Mise à jour locale du bouton
                        target.textContent = "Publié";
                        target.disabled = true;

                        // Si tu préfères recharger toute la liste, décommente la ligne suivante :
                        // await loadReviews();
                    } else {
                        alert("❌ Erreur lors de la publication.");
                    }
                } catch (error) {
                    alert("❌ Erreur réseau lors de la publication.");
                    console.error(error);
                }
            }
        }

        // --- Suppression d'une review ---
        if (target.classList.contains("btn-delete")) {
            if (confirm("Supprimer cette review ?")) {
                try {
                    const response = await fetch(`/reviews/delete/${id}`, {
                        method: "DELETE",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken,
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
        }
    });
    // Simple fonction d'échappement HTML pour éviter injection
    function escapeHtml(text) {
        if (!text) return "";
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

    // Chargement initial des reviews
    loadReviews();
});


