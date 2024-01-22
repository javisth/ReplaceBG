from PIL import Image

# Load the foreground image (with alpha channel) and background image
foreground = Image.open('path_to_foreground_image.png')  # Image with transparency
background = Image.open('path_to_background_image.jpg')  # New background image

# Resize background to match the size of the foreground image
background = background.resize(foreground.size)

# Paste the foreground onto the background
background.paste(foreground, (0, 0), foreground)

# Save the resulting image
background.save('path_to_result_image.png')

