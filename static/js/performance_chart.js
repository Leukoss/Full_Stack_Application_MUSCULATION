document.addEventListener('DOMContentLoaded', () => {
    // get the data for the chart
    const performancesDataElement = document.getElementById('performances-data');
    const performancesDataJSON = performancesDataElement.textContent;
    
    // from JSON to JS object
    const performancesData = JSON.parse(performancesDataJSON);

    // store the dates
    const labels = []; 
    const datasets = [];

    // compute the number maximal of set
    const maxSets = Math.max(...performancesData.map(p => p.weights.length));

    // for each set create a dataset
    for (let i = 0; i < maxSets; i++) {
        datasets.push({
            label: `Set ${i + 1}`,
            data: [],
            fill: false,
            borderColor: `hsl(${(i * 360 / maxSets)}, 100%, 50%)`, // dynamic colors
            tension: 0.1
        });
    }

    // fill data
    performancesData.forEach(performance => {
        labels.push(performance.date);
        performance.weights.forEach((weight, index) => {
            if (index < datasets.length) {
                datasets[index].data.push(weight); // Ajouter le poids pour chaque set
            }
        });
    });

    // creation of graphics
    const ctx = document.getElementById('performanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line', 
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Poids (kg)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'performances au fil du temps'
                }
            }
        }
    });
});
