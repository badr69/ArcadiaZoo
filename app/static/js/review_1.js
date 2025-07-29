document.addEventListener("DOMContentLoaded", () => {
    const reviewsList = document.querySelector("#Reviews-list");
    if (!reviewsList) return;

    // Récupération du token CSRF si nécessaire
    const csrfToken = document.querySelector('input[name="csrf_token"]')?.value || '';

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
                        <button class="btn-delete btn btn-danger btn-sm me-2" data-id="${review.id}">Delete</button>
                        <button class="btn-publish btn btn-primary btn-sm me-2" data-id="${review.id}">Publish</button>
                      </div>
                    </td>
                `;
                reviewsList.appendChild(tr);
            });
        } catch (error) {
            console.error("Erreur lors du chargement des reviews :", error);
        }
    }

    loadReviews();

    // Gestion des clics sur les boutons Publish et Delete
    reviewsList.addEventListener("click", async (event) => {
        const target = event.target;

        if (target.classList.contains("btn-publish")) {
            const id = target.getAttribute("data-id");
            if (!id) return;

            if (confirm("Publier cette review ?")) {
                try {
                    const response = await fetch(`/reviews/publish/${id}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken,
                        },
                    });
                    if (response.ok) {
                        alert("✅ Review publiée !");
                        target.disabled = true;
                        target.textContent = "Publié";
                    } else {
                        alert("❌ Erreur lors de la publication.");
                    }
                } catch (error) {
                    alert("❌ Erreur réseau lors de la publication.");
                    console.error(error);
                }
            }
        }

        if (target.classList.contains("btn-delete")) {
            const id = target.getAttribute("data-id");
            if (!id) return;

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
                        // Retirer la ligne du tableau
                        target.closest("tr").remove();
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
});

