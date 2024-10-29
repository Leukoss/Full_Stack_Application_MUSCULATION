document.addEventListener('DOMContentLoaded', function () {
    // initial count for set
    let setCount = 1; 

    // select all exercises
    const exerciseLinks = document.querySelectorAll('.exercise-link');
    
    const exercisePanel = document.querySelector('.exercise-panel');

    // tocken to create a form
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // function that 
    exerciseLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); 

            // get id and name of exercise 
            const exerciseId = this.getAttribute('data-id');
            const exerciseName = this.getAttribute('data-name');

            // Injecter le formulaire de performance dans l'exercise panel
            exercisePanel.innerHTML = `
                <h3>Nouvelle performance pour ${exerciseName.toLowerCase()}</h3>
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

            // number of set equals to 1
            setCount = 1;

            // select buttons to add set
            const addSetBtn = exercisePanel.querySelector('#add-set-btn');
            const setsContainer = exercisePanel.querySelector('#sets-container');

            // function which add a set
            addSetBtn.addEventListener('click', function () {
                // add one to the number of set
                setCount++; 

                // create a new element for the new set
                const newSetDiv = document.createElement('div');
                newSetDiv.classList.add('set');

                // create label for the new set
                newSetDiv.innerHTML = `
                    <label>Set ${setCount} :</label>
                    <input type="text" name="weights" placeholder="Poids (kg)">
                    <input type="text" name="repetitions" placeholder="Répétitions">
                `;

                setsContainer.appendChild(newSetDiv);
            });
        });
    });
});
