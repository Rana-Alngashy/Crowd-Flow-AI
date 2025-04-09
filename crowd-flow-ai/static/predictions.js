document.addEventListener('DOMContentLoaded', () => {
    const data = JSON.parse(sessionStorage.getItem('crowdData'));
    if (!data) {
        window.location.href = '/';
        return;
    }

    const ctx = document.getElementById('predictionChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Now', '5 min', '10 min', '15 min', '20 min'],
            datasets: Object.entries(data.predictions).map(([gate, values], i) => ({
                label: gate,
                data: values.map(Math.round),
                borderColor: ['#007bff', '#28a745', '#dc3545'][i],
                tension: 0.3
            }))
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    document.getElementById('prediction-data').innerHTML = `
        ${Object.entries(data.predictions).map(([gate, values]) => `
            <div class="gate-prediction">
                <h4>${gate}</h4>
                <ul>
                    ${values.map((val, i) => 
                      `<li>${['Now', '5 min', '10 min', '15 min', '20 min'][i]}: ${Math.round(val)} people</li>`
                    ).join('')}
                </ul>
            </div>
        `).join('')}
    `;
});