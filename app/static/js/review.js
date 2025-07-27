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

    async function loadReviews() {
        try {
            const response = await fetch("/reviews"); // route GET pour récupérer toutes les reviews
            if (!response.ok) throw new Error("Erreur de chargement des reviews");
            const reviews = await response.json();

            const reviewsList = document.querySelector("#Reviews-list");
            if (!reviewsList) return;

            reviewsList.innerHTML = ""; // vide la liste avant de la remplir

            reviews.forEach(review => {
                const div = document.createElement("div");
                div.classList.add("review-item");
                div.innerHTML = `
                    <strong>${review.pseudo}</strong> — note : ${review.rating} <br>
                    <p>${review.message}</p>
                    <small>${new Date(review.date).toLocaleString()}</small>
                `;
                reviewsList.appendChild(div);
            });
        } catch (err) {
            console.error(err);
        }
    }

    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        console.log("Submit intercepté !");

        const csrfToken = form.querySelector('input[name="csrf_token"]').value;
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

                await loadReviews(); // recharge la liste complète
            } else {
                alert("Erreur : " + (data.error || "Impossible d’envoyer la review."));
            }
        } catch (err) {
            alert("Erreur lors de l’envoi de la review.");
            console.error(err);
        }
    });

    loadReviews(); // charge les reviews au chargement de la page
});





// document.addEventListener("DOMContentLoaded", () => {
//     const form = document.querySelector("#form-review");
//     const pseudoInput = document.querySelector("#pseudo");
//     const messageInput = document.querySelector("#text-area-review");
//     const ratingInput = document.querySelector("#rating");
//     const submitBtn = document.querySelector("#submit-btn");
//
//     submitBtn.disabled = true;
//
//     function validateForm() {
//         submitBtn.disabled = !(pseudoInput.value.trim() && messageInput.value.trim() && ratingInput.value.trim());
//     }
//
//     pseudoInput.addEventListener("keyup", validateForm);
//     messageInput.addEventListener("keyup", validateForm);
//     ratingInput.addEventListener("change", validateForm);
//
//     form.addEventListener("submit", async function(event) {
//         event.preventDefault();
//         console.log("Submit intercepté !");
//
//         const csrfToken = form.querySelector('input[name="csrf_token"]').value;
//         const pseudo = pseudoInput.value.trim();
//         const message = messageInput.value.trim();
//         const rating = ratingInput.value.trim();
//
//         try {
//             const response = await fetch("/reviews/submit_review", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-Requested-With": "XMLHttpRequest",
//                     "X-CSRFToken": csrfToken
//                 },
//                 body: JSON.stringify({ pseudo, message, rating }),
//             });
//
//             const data = await response.json();
//
//             console.log("Données envoyées:", { pseudo, message, rating });
//             console.log("Réponse serveur:", data);
//
//             if (response.ok) {
//                 alert("Votre review a bien été envoyée !");
//                 form.reset();
//                 submitBtn.disabled = true;
//
//
//                 // Ajout dynamique de la nouvelle review dans la liste
//                 const reviewsList = document.querySelector("#Reviews-list");
//                 if (reviewsList) {
//                     const newReview = document.createElement("div");
//                     newReview.classList.add("review-item");
//                     newReview.innerHTML = `
//                         <strong>${pseudo}</strong> — note : ${rating} <br>
//                         <p>${message}</p>
//                         <small>À l'instant</small>
//                     `;
//                     reviewsList.prepend(newReview);
//                 }
//
//             } else {
//                 alert("Erreur : " + (data.error || "Impossible d’envoyer la review."));
//             }
//         } catch (err) {
//             alert("Erreur lors de l’envoi de la review.");
//             console.error(err);
//         }
//     });
// });
