Webcam.set({
    width: 640,
    height: 480,
    image_format: 'jpeg',
    jpeg_quality: 90
});
Webcam.attach('#my_camera');

document.getElementById('captureButton').addEventListener('click', function() {
    Webcam.snap(function(data_uri) {
        // Display captured image
        document.getElementById('results').innerHTML = 
            '<img id="capturedImage" src="'+data_uri+'"/>';

        // You can also send 'data_uri' to the server using a POST request
    });
});
