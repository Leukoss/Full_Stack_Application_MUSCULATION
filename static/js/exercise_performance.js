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
            fetch(`/exercise/${exerciseId}/get_last_performances`)
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    // if there is at least one performances
                    if (data.performances.length > 0) {              

                        let table = `<h3>Performances ${exerciseName}</h3>`;
                        
                        table += '<table border="1">';
                        table += '<thead><tr><th>Date</th>';

                        // add columns for each set
                        for (let i = 0; i < data.max_sets; i++) {
                            table += `<th>Set ${i+1} </th>`;
                        }
                        table += '</tr></thead>';

                        
                        table += '<tbody>';
                        data.performances.forEach(performance => {
                            table += `<tr><td>${performance.date}</td>`;

                            performance.weights.forEach((weight, index) => {
                
                                if (weight !== null && performance.repetitions[index] !== null) {

                                    table += `<td>${performance.repetitions[index]} x ${weight} kg</td>`;
                                } else {
                                    table += '<td>-</td>'; 
                                }
                            });
                        });
                        table += '</tbody></table>';

                        exercisePanel.innerHTML = table;

                        exercisePanel.innerHTML += `<div><a href="/exercise/${exerciseId}/detail" class="see-more">Voir plus</a></div>`;

                    } else {
                        // no performances found
                        exercisePanel.innerHTML = '<p>Aucune performance trouvée pour cet exercice.</p>';
                    }
                })
                .catch(error => {
                    console.error('Erreur lors de la récupération des performances:', error);
                    exercisePanel.innerHTML = '<p>Pas de performances enregistrées</p>';
                });
        });
    });
});
