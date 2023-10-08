document.addEventListener('DOMContentLoaded', function () {
    const videoElement = document.getElementById('camera-preview');
    const imageDataInput = document.getElementById('image-data');
    const cameraUploadInput = document.getElementById('camera-upload');
    const fileUploadInput = document.getElementById('file-upload');
    const captureButton = document.getElementById('capture-button');
    const uploadButton = document.getElementById('upload-button');
    const uploadMessage = document.getElementById('upload-message');

    // Check if the user's browser supports getUserMedia
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Access the user's camera
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;
            })
            .catch(function (error) {
                console.error('Error accessing camera:', error);
            });

        // Capture an image when the button is clicked
        captureButton.addEventListener('click', function () {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

            // Convert the canvas image to a data URL (base64)
            const imageDataUrl = canvas.toDataURL('image/jpeg');

            // Set the captured image data in the hidden input field
            imageDataInput.value = imageDataUrl;
            uploadMessage.style.display = 'block';
            uploadMessage.textContent = 'Image captured successfully!';
        });

        // Show the camera upload dialog when the button is clicked
        uploadButton.addEventListener('click', function () {
            cameraUploadInput.click();
        });
    } else {
        console.error('getUserMedia is not supported in this browser.');
    }

    // Handle file selection from the camera input
    cameraUploadInput.addEventListener('change', function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            // Read the selected file as a data URL
            const reader = new FileReader();
            reader.onload = function (e) {
                // Set the selected image data in the hidden input field
                imageDataInput.value = e.target.result;
                uploadMessage.style.display = 'block';
                uploadMessage.textContent = 'Image uploaded successfully!';
            };
            reader.readAsDataURL(selectedFile);
        }
    });

    // Handle file selection from the computer input
    fileUploadInput.addEventListener('change', function (event) {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            // Read the selected file as a data URL
            const reader = new FileReader();
            reader.onload = function (e) {
                // Set the selected image data in the hidden input field
                imageDataInput.value = e.target.result;
                uploadMessage.style.display = 'block';
                uploadMessage.textContent = 'Image uploaded successfully!';
            };
            reader.readAsDataURL(selectedFile);
        }
    });
});
