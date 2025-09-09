document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.animal-clickable');

    images.forEach(img => {
        img.addEventListener('click', () => {
            const animalId = img.dataset.animalId;

            fetch(`/animal_click/${animalId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Si CSRF est activé, ajoute ici l'en-tête X-CSRFToken
                    'X-CSRFToken': '{{ csrf_token() }}'
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (response.ok) {
                    console.log(`Click enregistré pour animal ${animalId}`);
                } else {
                    console.error('Erreur lors de l\'enregistrement du clic');
                }
            })
            .catch(error => console.error('Erreur réseau:', error));
        });
    });
});