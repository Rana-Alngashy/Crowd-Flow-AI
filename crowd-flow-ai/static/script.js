document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading spinner
    const overlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    overlay.style.display = 'flex';
    
    try {
        const formData = new FormData();
        let hasVideo = false;
        
        // Check if any file is a video
        for (let i = 1; i <= 3; i++) {
            const file = document.getElementById(`file${i}`).files[0];
            formData.append(`file${i}`, file);
            if (file && file.type.includes('video')) {
                hasVideo = true;
                loadingText.textContent = "Analyzing video (this may take a moment)...";
            }
        }

        const response = await fetch('/crowd-data', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Server error');
        const data = await response.json();

        // Store data and redirect
        sessionStorage.setItem('crowdData', JSON.stringify(data));
        window.location.href = '/analysis';

    } catch (error) {
        console.error(error);
        alert('Error processing files. Check console for details.');
    } finally {
        overlay.style.display = 'none'; // Hide spinner when done
    }
});