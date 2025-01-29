const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureBtn = document.getElementById('capture-btn');
const imageInput = document.getElementById('image-input');
const uploadForm = document.getElementById('upload-form');

// Ellipse properties
const ellipseX = canvas.width / 2;
const ellipseY = canvas.height / 2;
const ellipseRadiusX = 150;
const ellipseRadiusY = 200;

// Start the camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing the camera: ", err);
    });

// Draw ellipse on the canvas
function drawEllipse() {
    context.beginPath();
    context.ellipse(ellipseX, ellipseY, ellipseRadiusX, ellipseRadiusY, 0, 0, 2 * Math.PI);
    context.strokeStyle = 'green';
    context.lineWidth = 3;
    context.stroke();
}

// Capture image inside the ellipse
captureBtn.addEventListener('click', () => {
    // Draw the current video frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Create a temporary canvas to crop the ellipse
    const tempCanvas = document.createElement('canvas');
    const tempContext = tempCanvas.getContext('2d');
    tempCanvas.width = ellipseRadiusX * 2;
    tempCanvas.height = ellipseRadiusY * 2;

    // Draw the ellipse region onto the temporary canvas
    tempContext.beginPath();
    tempContext.ellipse(
        ellipseRadiusX, ellipseRadiusY, ellipseRadiusX, ellipseRadiusY, 0, 0, 2 * Math.PI
    );
    tempContext.clip();
    tempContext.drawImage(
        canvas,
        ellipseX - ellipseRadiusX, ellipseY - ellipseRadiusY,
        ellipseRadiusX * 2, ellipseRadiusY * 2,
        0, 0,
        ellipseRadiusX * 2, ellipseRadiusY * 2
    );

    // Convert the cropped image to a data URL
    const croppedImage = tempCanvas.toDataURL('image/png');
    imageInput.value = croppedImage;

    // Submit the form
    uploadForm.submit();
});

// Continuously draw the ellipse on the video feed
function draw() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    drawEllipse();
    requestAnimationFrame(draw);
}

// Start drawing
draw();