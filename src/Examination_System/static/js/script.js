const video = document.getElementById('video');
let unknownFaceTime = 0;
let lastUpdateTime = Date.now();
let count = 0;

Promise.all([
    faceapi.nets.ssdMobilenetv1.loadFromUri("/static/models"),
    faceapi.nets.faceRecognitionNet.loadFromUri("/static/models"),
    faceapi.nets.faceLandmark68Net.loadFromUri("/static/models"),
]).then(startWebcam).then(faceRecognition).then(updateUnknownFacePercentage);

function startWebcam() {
    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
    })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing the camera:', error);
        });

    setInterval(updateUnknownFacePercentage, 1000); // Update percentage every second
}

function getLabeledFaceDescriptions() {
    const labels = ["Samin"];
    return Promise.all(
        labels.map(async (label) => {
            const descriptions = [];
            for (let i = 1; i <= 5; i++) {
                const img = await faceapi.fetchImage(`/static/labels/${label}/${i}.png`);
                const detections = await faceapi
                    .detectSingleFace(img)
                    .withFaceLandmarks()
                    .withFaceDescriptor();
                descriptions.push(detections.descriptor);
            }
            return new faceapi.LabeledFaceDescriptors(label, descriptions);
        })
    );
}

async function faceRecognition() {
    const labeledFaceDescriptors = await getLabeledFaceDescriptions();
    const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors);

    video.addEventListener('play', () => {
        const overlayCanvas = document.getElementById('overlayCanvas');
        const displaySize = { width: video.videoWidth, height: video.videoHeight };

        overlayCanvas.width = video.videoWidth;
        overlayCanvas.height = video.videoHeight;
        faceapi.matchDimensions(overlayCanvas, displaySize);

        setInterval(async () => {
            const currentTime = Date.now();
            const detections = await faceapi.detectAllFaces(video).withFaceLandmarks().withFaceDescriptors();
            const resizedDetections = faceapi.resizeResults(detections, displaySize);

            const context = overlayCanvas.getContext('2d');
            context.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

            resizedDetections.forEach((d) => {
                const result = faceMatcher.findBestMatch(d.descriptor);
                const box = d.detection.box;

                let string = result.toString();

                if (string.slice(0, 7) === 'unknown') {
                    unknownFaceTime += (currentTime - lastUpdateTime); // Update unknown time
                    count += 1;
                }
                new faceapi.draw.DrawBox(box, { label: count.toString() }).draw(overlayCanvas);
            });

            lastUpdateTime = currentTime; // Update last update time

        }, 100);
    });
}

function updateUnknownFacePercentage() {
    const currentTime = Date.now();
    const totalTime = currentTime - lastUpdateTime; // Update total time
    const unknownPercentage = ((unknownFaceTime/1000) / totalTime) * 100 ;
    document.getElementById('unknown-face-percentage').innerText = `Unknown face percentage: ${unknownPercentage.toFixed(2)}%`;
    document.getElementById('unknown-face-percentage_').value = unknownPercentage.toFixed(2)

    const debugInfo = `Unknown Face Time: ${unknownFaceTime}, Total Time: ${totalTime}, Percentage: ${unknownPercentage.toFixed(2)}%`;

    document.getElementById('debug-info').innerText = debugInfo;

}

updateUnknownFacePercentage();

