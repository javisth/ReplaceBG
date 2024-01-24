import subprocess
from PIL import Image
import os

def process_image(input_image_path, output_image_path, background_image_path):
    try:
        # Step 1: Use backgroundremover to remove the background
        temp_output_path = os.path.join(os.path.dirname(input_image_path), "temp_no_bg.png")
        subprocess.run([
            'backgroundremover',
            '-i', input_image_path,
            '-m', 'u2net_human_seg',
            '-o', temp_output_path
        ], check=True)

        # Step 2: Overlay the transparent image onto a new background using PIL
        foreground = Image.open(temp_output_path).convert("RGBA")
        background = Image.open(background_image_path).convert("RGBA")
        background = background.resize(foreground.size)

        # Combine foreground and background
        combined = Image.alpha_composite(background, foreground)
        combined.save(output_image_path, "PNG")
        
        os.remove(temp_output_path)  # Clean up temporary file

        return True
    except subprocess.CalledProcessError as e:
        print("Error in background removal:", e.stderr.decode())
        return False
    except Exception as e:
        print("Error in image processing:", str(e))
        return False

