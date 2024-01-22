function overlayImages(foregroundSrc, backgroundSrc, callback) {
    // Create image objects for foreground and background
    var foregroundImage = new Image();
    var backgroundImage = new Image();

    // Load foreground image
    foregroundImage.onload = function() {
        // Load background image
        backgroundImage.onload = function() {
            // Create a canvas
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');

            // Set canvas size to match background image size
            canvas.width = backgroundImage.width;
            canvas.height = backgroundImage.height;

            // Draw the background image
            ctx.drawImage(backgroundImage, 0, 0);

            // Draw the foreground image
            ctx.drawImage(foregroundImage, 0, 0, foregroundImage.width, foregroundImage.height);

            // Callback with the result
            callback(canvas.toDataURL());
        };

        // Set source of background image
        backgroundImage.src = backgroundSrc;
    };

    // Set source of foreground image
    foregroundImage.src = foregroundSrc;
}

// Example usage
overlayImages('path_to_foreground_image.png', 'path_to_background_image.jpg', function(resultImageSrc) {
    // Use resultImageSrc as the source for an image element or for further processing
    console.log('Overlay complete. Image source:', resultImageSrc);
});
