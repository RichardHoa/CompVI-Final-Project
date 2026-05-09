const video          = document.getElementById('webcamVideo');
const canvas         = document.getElementById('webcamCanvas');
const startWebcamBtn = document.getElementById('startWebcamBtn');
const captureBtn     = document.getElementById('captureBtn');
const loadingDiv     = document.getElementById('loading');
const resultsDiv     = document.getElementById('results');
const uploadPanel    = document.getElementById('upload-panel');

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
    canvas.width  = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    canvas.toBlob(async (blob) => {
        const fd = new FormData();
        fd.append("file", blob, "webcam.png");
        await sendToAnalyze(fd);
    }, 'image/png');
});

document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('imageInput');
    if (!fileInput.files.length) { alert("Please select an image file first."); return; }
    const fd = new FormData();
    fd.append("file", fileInput.files[0]);
    await sendToAnalyze(fd);
});

document.getElementById('analyzeAgainBtn').addEventListener('click', () => {
    resultsDiv.classList.add('hidden');
    uploadPanel.style.display = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

async function sendToAnalyze(formData) {
    uploadPanel.style.display = 'none';
    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');

    try {
        const response = await fetch('/analyze', { method: 'POST', body: formData });
        const data     = await response.json();

        loadingDiv.classList.add('hidden');

        if (!response.ok || data.error) {
            uploadPanel.style.display = '';
            alert(data.error || `Server error: ${response.statusText}`);
            return;
        }

        if (data.status === "success") {
            renderResults(data.data || data);
            resultsDiv.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    } catch (err) {
        console.error(err);
        uploadPanel.style.display = '';
        loadingDiv.classList.add('hidden');
        alert("An error occurred during analysis.");
    }
}

function renderResults(d) {
    const features       = d.features       || {};
    const interpretation = d.interpretation || {};
    const stageImages    = d.stage_images   || {};

    /* ── Hero images ───────────────────────────────── */
    const vizImg = document.getElementById('visualizedImage');
    if (d.visualization_url) {
        vizImg.src = d.visualization_url + '?t=' + Date.now();
    }
    setImg('sketchImg', stageImages['edges.png']);

    /* ── Overview summary cards ────────────────────── */
    const fi = interpretation.face || [];
    const ei = interpretation.eye  || [];
    const li = interpretation.lip  || [];
    const ti = interpretation.thirds || [];
    const ni = interpretation.nose || [];

    const overviewEl = document.getElementById('overviewItems');
    overviewEl.innerHTML = '';
    [
        { icon: '⚏', cls: 'thirds-icon', region: 'Tỉ Lệ Mặt', primary: ti[ti.length-1], sub: ti.slice(0, -1).join(' · ') },
        { icon: '◇', cls: 'face-icon', region: 'Khuôn Mặt', primary: fi[0], sub: fi.slice(1).join(' · ') },
        { icon: '△', cls: 'nose-icon', region: 'Mũi', primary: ni[0], sub: ni.slice(1).join(' · ') },
        { icon: '◎', cls: 'eye-icon',  region: 'Đôi Mắt',   primary: ei[0], sub: ei.slice(1).join(' · ') },
        { icon: '♡', cls: 'lip-icon',  region: 'Đôi Môi',   primary: li[0], sub: li.slice(1).join(' · ') },
    ].forEach(r => {
        const row = document.createElement('div');
        row.className = 'overview-row';
        row.innerHTML = `
            <span class="ov-icon ${r.cls}">${r.icon}</span>
            <div>
                <div class="ov-region">${r.region}</div>
                <div class="ov-value">${r.primary || '—'}</div>
                ${r.sub ? `<div class="ov-sub">${r.sub}</div>` : ''}
            </div>`;
        overviewEl.appendChild(row);
    });

    /* ── Crop images ───────────────────────────────── */
    setImg('faceCropImg',  stageImages['face_crop.png']);
    setImg('leftEyeImg',   stageImages['left_eye_crop.png']);
    setImg('rightEyeImg',  stageImages['right_eye_crop.png']);
    setImg('lipImg',       stageImages['lip_crop.png']);
    setImg('noseImg',      stageImages['nose_crop.png']);

    /* ── Face metrics & interpretation ─────────────── */
    renderMetrics('faceMetrics', features.face, [
        { key: 'L',             label: 'Length ratio' },
        { key: 'J',             label: 'Jaw ratio' },
        { key: 'F',             label: 'Forehead ratio' },
        { key: 'symmetry_diff', label: 'Symmetry diff' },
    ]);
    renderInterp('faceInterpDetail', fi);

    /* ── Eye metrics & interpretation ──────────────── */
    renderMetrics('eyeMetrics', features.eye, [
        { key: 'ratio',            label: 'H/W ratio' },
        { key: 'tilt',             label: 'Tilt (°)' },
        { key: 'gap_ratio',        label: 'Inter-eye gap' },
        { key: 'horizontal_score', label: 'Eyelid score' },
    ]);
    renderInterp('eyeInterpDetail', ei);

    /* ── Lip metrics & interpretation ──────────────── */
    renderMetrics('lipMetrics', features.lip, [
        { key: 'lip_ratio', label: 'H/W ratio' },
        { key: 'tb_ratio',  label: 'Top / Bottom ratio' },
        { key: 'bow_depth', label: 'Cupid bow depth' },
    ]);
    renderInterp('lipInterpDetail', li);

    /* ── Thirds metrics & interpretation ─────────────── */
    renderMetrics('thirdsMetrics', features.thirds, [
        { key: 'upper_ratio',   label: 'Upper Face' },
        { key: 'middle_ratio',  label: 'Middle Face' },
        { key: 'lower_ratio',   label: 'Lower Face' },
        { key: 'balance_score', label: 'Balance Score' },
    ]);
    renderInterp('thirdsInterpDetail', ti);

    /* ── Nose metrics & interpretation ──────────────── */
    renderMetrics('noseMetrics', features.nose, [
        { key: 'width_ratio',       label: 'Width ratio' },
        { key: 'length_ratio',      label: 'Length ratio' },
        { key: 'tip_ratio',         label: 'Tip ratio' },
        { key: 'bridge_projection', label: 'Bridge proj.' },
        { key: 'confidence',        label: 'Confidence' },
    ]);
    renderInterp('noseInterpDetail', ni);
}

function renderMetrics(containerId, feats, defs) {
    const el = document.getElementById(containerId);
    el.innerHTML = '';
    if (!feats) return;
    defs.forEach(({ key, label }) => {
        if (feats[key] === undefined) return;
        const val = typeof feats[key] === 'number' ? feats[key].toFixed(3) : feats[key];
        const row = document.createElement('div');
        row.className = 'metric-row';
        row.innerHTML = `<span class="metric-label">${label}</span><span class="metric-value">${val}</span>`;
        el.appendChild(row);
    });
}

function renderInterp(containerId, labels) {
    const el = document.getElementById(containerId);
    el.innerHTML = '';
    (labels || []).forEach(text => {
        const item = document.createElement('div');
        item.className = 'interp-item';
        item.innerHTML = `<span class="interp-bullet">•</span><span class="interp-text">${text}</span>`;
        el.appendChild(item);
    });
}

function setImg(id, url) {
    const el = document.getElementById(id);
    if (!el) return;
    if (url) { el.src = url; el.style.display = ''; }
    else      { el.style.display = 'none'; }
}
