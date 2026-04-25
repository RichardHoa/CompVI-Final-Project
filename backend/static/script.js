document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('imageInput');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const featuresList = document.getElementById('featuresList');
    const interpretationList = document.getElementById('interpretationList');

    if (fileInput.files.length === 0) {
        alert("Please select an image file first.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    // Show loading
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');

    try {
        // We assume the FastAPI backend runs on localhost:8000
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Hide loading, show results
        loadingDiv.classList.add('hidden');
        resultsDiv.classList.remove('hidden');

        // Clear previous results
        featuresList.innerHTML = '';
        interpretationList.innerHTML = '';

        if (data.status === "success") {
            // Render features
            for (const [key, value] of Object.entries(data.data.features)) {
                const li = document.createElement('li');
                li.textContent = `${key}: ${value}`;
                featuresList.appendChild(li);
            }

            // Render interpretations
            data.data.interpretation.forEach(text => {
                const li = document.createElement('li');
                li.textContent = text;
                interpretationList.appendChild(li);
            });
        }

    } catch (error) {
        console.error("Error during analysis:", error);
        alert("An error occurred. Make sure the FastAPI backend is running.");
        loadingDiv.classList.add('hidden');
    }
});
