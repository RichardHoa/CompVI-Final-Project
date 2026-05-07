const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const featuresList = document.getElementById('featuresList');
const interpretationList = document.getElementById('interpretationList');
const visualizedImage = document.getElementById('visualizedImage');

const video = document.getElementById('webcamVideo');
const canvas = document.getElementById('webcamCanvas');
const startWebcamBtn = document.getElementById('startWebcamBtn');
const captureBtn = document.getElementById('captureBtn');

let stream = null;

startWebcamBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.style.display = 'block';
        captureBtn.style.display = 'inline-block';
        startWebcamBtn.style.display = 'none';
    } catch (err) {
        alert("Cannot access webcam: " + err);
    }
});

captureBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob, "webcam.png");
        await sendToAnalyze(formData);
    }, 'image/png');
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('imageInput');
    if (fileInput.files.length === 0) {
        alert("Please select an image file first.");
        return;
    }
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    await sendToAnalyze(formData);
});

async function sendToAnalyze(formData) {
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    featuresList.innerHTML = '';
    interpretationList.innerHTML = '';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        loadingDiv.classList.add('hidden');

        if (!response.ok || data.error) {
            alert(data.error || `Server error: ${response.statusText}`);
            return;
        }

        resultsDiv.classList.remove('hidden');

        if (data.status === "success") {
            let actualData = data.data || data;
            
            // Render nested features
            const renderFeatures = (obj, prefix = '') => {
                for (const [key, value] of Object.entries(obj)) {
                    if (typeof value === 'object' && value !== null) {
                        renderFeatures(value, `${prefix}${key} - `);
                    } else {
                        const li = document.createElement('li');
                        const valStr = typeof value === 'number' ? value.toFixed(2) : value;
                        li.textContent = `${prefix}${key}: ${valStr}`;
                        featuresList.appendChild(li);
                    }
                }
            };
            if(actualData.features) renderFeatures(actualData.features);
            
            // Render visualization image with cache-busting
            if(actualData.visualization_url) {
                visualizedImage.src = actualData.visualization_url + '?t=' + new Date().getTime();
            }

            // Render interpretations (nested array)
            if(actualData.interpretation) {
                for (const [key, value] of Object.entries(actualData.interpretation)) {
                    value.forEach(text => {
                        const li = document.createElement('li');
                        li.textContent = `[${key}] ${text}`;
                        interpretationList.appendChild(li);
                    });
                }
            }
        }
    } catch (error) {
        console.error(error);
        alert("An error occurred during analysis.");
        loadingDiv.classList.add('hidden');
    }
}
