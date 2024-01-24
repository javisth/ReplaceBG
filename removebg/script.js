document.getElementById('captureButton').addEventListener('click', () => {
    console.log('Button clicked'); // Add this line
    const constraints = {
        video: true
    };

    const video = document.createElement('video');

    navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
      console.log('Camera access granted'); // Add this line
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
            };
        })
        .catch((error) => {
            console.error('Error accessing the camera: ', error);
        });

    document.body.appendChild(video);
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    video.addEventListener('playing', () => {
        setTimeout(() => {
            console.log('Taking photo...'); // Add this line
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imgData = canvas.toDataURL('image/png');
            console.log('Image captured:', imgData); // Add this line
            video.srcObject.getTracks().forEach(track => track.stop());
            document.body.removeChild(video);
        }, 100);
    });
});
