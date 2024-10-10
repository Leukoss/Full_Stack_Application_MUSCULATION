document.addEventListener('DOMContentLoaded', function () {
    const exerciseLinks = document.querySelectorAll('.exercise-link');
    const exercisePanel = document.querySelector('.exercise-panel');

    // For each link of exercises
    exerciseLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            
            // prevent loading of the page
            event.preventDefault(); 
            // get the id of the exercise
            const exerciseId = this.getAttribute('data-id');
            // get the name of the exercise
            const exerciseName = this.getAttribute('data-name').toLowerCase();

            // send a request
            fetch(`/exercise/${exerciseId}/performances`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    // if there is at least one performances
                    if (data.performances.length > 0) {
                        // Calculer le max_sets
                        let max_sets = 0;
                        data.performances.forEach(performance => {
                            // Vérifie que weights est bien un tableau
                            if (Array.isArray(performance.weights)) {
                                // Met à jour max_sets si la longueur de weights est plus grande
                                const setsCount = performance.weights.length;
                                if (setsCount > max_sets) {
                                    max_sets = setsCount;
                                }
                            }
                        });
                        // update
                        let table = `<h3>Performances ${exerciseName}</h3>`;
                        // Créer le tableau HTML avec les colonnes pour chaque set et les lignes pour chaque date
                        table += '<table border="1">';
                        table += '<thead><tr><th>Date</th>';
                        // Ajouter les colonnes pour chaque set
                        for (let i = 0; i < max_sets; i++) {
                            table += `<th>Set ${i+1} </th>`;
                        }
                        table += '</tr></thead>';

                        // Ajouter les lignes pour chaque performance
                        table += '<tbody>';
                        data.performances.forEach(performance => {
                            table += `<tr><td>${performance.date}</td>`;
                            // Boucle à travers les poids et les répétitions
                            performance.weights.forEach((weight, index) => {
                                // Vérifiez si le poids et les répétitions existent
                                if (weight !== null && performance.repetitions[index] !== null) {
                                    // Formatez l'affichage comme '12 x 60 kg'
                                    table += `<td>${performance.repetitions[index]} x ${weight} kg</td>`;
                                } else {
                                    table += '<td>-</td>'; // Si pas de poids ou de répétition pour ce set
                                }
                            });

                            // If the current performance has fewer sets than the max, add empty cells with '-'
                            const missingSets = max_sets - performance.weights.length;
                            for (let i = 0; i < missingSets; i++) {
                                table += '<td>-</td>';
                            }
                            table += '</tr>';
                        });
                        table += '</tbody></table>';

                        // Afficher le tableau dans l'exercise-panel
                        exercisePanel.innerHTML = table;
                    } else {
                        // no performances found
                        exercisePanel.innerHTML = '<p>Aucune performance trouvée pour cet exercice.</p>';
                    }
                })
                .catch(error => {
                    console.error('Erreur lors de la récupération des performances:', error);
                    exercisePanel.innerHTML = '<p>Erreur lors de la récupération des performances.</p>';
                });
        });
    });
});
