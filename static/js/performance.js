document.addEventListener('DOMContentLoaded', function () {
    let setCount = 1; // Initial set count

    // Sélectionner tous les liens d'exercice
    const exerciseLinks = document.querySelectorAll('.exercise-link');
    
    // Sélectionner le panel où afficher le formulaire
    const exercisePanel = document.querySelector('.exercise-panel');

    // Récupérer le jeton CSRF depuis le HTML (inclus dans le template)
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Fonction pour afficher et injecter le formulaire de performance
    exerciseLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Empêche le comportement par défaut du lien

            // Récupérer l'ID et le nom de l'exercice
            const exerciseId = this.getAttribute('data-id');
            const exerciseName = this.getAttribute('data-name');

            // Injecter le formulaire de performance dans l'exercise panel
            exercisePanel.innerHTML = `
                <h3>Nouvelle performance pour ${exerciseName}</h3>
                <form id='performance-form-${exerciseId}' method="POST" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                    <input type="hidden" name="exercise_id" value="${exerciseId}">
                    <div id="sets-container">
                        <!-- La première série est déjà présente -->
                        <div class="set">
                            <label>Set 1 :</label>
                            <input type="text" name="weights" placeholder="Poids (kg)">
                            <input type="text" name="repetitions" placeholder="Répétitions">
                        </div>
                    </div>
                    <button type="button" id="add-set-btn" class="btn">Ajouter une série</button>
                    <button type="submit" name="performance" class="btn">Soumettre</button>
                </form>
            `;

            // Réinitialiser le compteur de sets
            setCount = 1;

            // Sélectionner le bouton pour ajouter des séries
            const addSetBtn = exercisePanel.querySelector('#add-set-btn');
            const setsContainer = exercisePanel.querySelector('#sets-container');

            // Fonction pour ajouter une nouvelle série
            addSetBtn.addEventListener('click', function () {
                setCount++; // Incrémenter le compteur de séries

                // Créer un nouveau div pour la nouvelle série
                const newSetDiv = document.createElement('div');
                newSetDiv.classList.add('set');

                // Ajouter les labels et les champs pour les répétitions et les poids
                newSetDiv.innerHTML = `
                    <label>Set ${setCount} :</label>
                    <input type="text" name="weights" placeholder="Poids (kg)">
                    <input type="text" name="repetitions" placeholder="Répétitions">
                `;

                // Ajouter le nouveau div dans le conteneur de séries
                setsContainer.appendChild(newSetDiv);
            });
        });
    });
});
