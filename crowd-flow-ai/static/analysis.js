document.addEventListener('DOMContentLoaded', () => {
    const data = JSON.parse(sessionStorage.getItem('crowdData'));
    if (!data) {
        window.location.href = '/';
        return;
    }

    document.getElementById('crowd-counts').innerHTML = `
        ${Object.entries(data.gates).map(([gate, count]) => 
          `<p>${gate}: <strong>${Math.round(count)}</strong> people 
           (<span class="movement">${data.movement[gate]}</span>)</p>`).join('')}
    `;

    document.getElementById('heatmap').src = data.heatmap;

    document.getElementById('recommendation').innerHTML = `
        <p><strong>Best Gate (Least Congested):</strong> ${data.recommended_gate}</p>
    `;
});