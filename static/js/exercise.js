document.addEventListener('DOMContentLoaded', function () {
    const exerciseLinks = document.querySelectorAll('.exercise-link');
    const exercisePanel = document.querySelector('.exercise-panel');

    // for each exercise link
    exerciseLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            // prevent loading of the pafz
            event.preventDefault(); 
            const exerciseId = this.getAttribute('data-id');

            // request of the exercise
            fetch(`/exercise/${exerciseId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        exercisePanel.innerHTML = `<p>${data.error}</p>`;
                    } else {
                        exercisePanel.innerHTML = `
                            <h3>${data.name}</h3>
                            ${data.illustration ? `<img src="${data.illustration}" alt="Illustration de l'exercice">` : '<p>Pas d\'illustration disponible</p>'}
                        `;
                    }
                })
                .catch(error => {
                    console.error('Erreur lors de la récupération des détails de l\'exercice:', error);
                });
        });
    });
});
