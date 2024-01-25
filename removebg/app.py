from flask import Flask, request, jsonify, send_file, url_for
from flask_cors import CORS
import background_remover  # Your background removal module
from PIL import Image
import qrcode
import os
from io import BytesIO
import base64

app = Flask(__name__, static_folder='static')  # Set the static_folder to 'static'
CORS(app)

output_dir = 'output'
backgrounds_dir = 'berlin'  # Adjust this to your backgrounds directory
logo_path = 'logo.png'  # Path to your logo image
os.makedirs(os.path.join(app.static_folder, output_dir), exist_ok=True)  # Ensure the output directory exists

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    background_filename = request.form.get('background')
    if not background_filename:
        return jsonify({'error': 'No background selected'}), 400

    image = request.files['image']
    input_path = os.path.join(app.static_folder, output_dir, 'input_image.jpg')
    output_path = os.path.join(app.static_folder, output_dir, 'output_image.png')
    background_path = os.path.join(backgrounds_dir, background_filename)

    image.save(input_path)

    # Process the image with background removal, adding logo and QR code
    if background_remover.process_image(input_path, output_path, background_path):
        final_image_path = process_image_with_logo_and_qr(output_path, output_path, 
                                                          background_path, logo_path, 
                                                          'https://www.redbull.com/in-en/event-series/red-bull-can-you-make-it?filter.countryCode=IN')

        if final_image_path is not None:
            # Generate QR Code for the view image page
            view_image_url = url_for('view_image', filename='output_image.png', _external=True)
            qr_code_img = generate_qr_code(view_image_url)
            qr_io = BytesIO()
            qr_code_img.save(qr_io, 'PNG')
            qr_io.seek(0)
            qr_code_data_url = 'data:image/png;base64,' + base64.b64encode(qr_io.getvalue()).decode()

            image_url = url_for('static', filename=f'{output_dir}/output_image.png', _external=True)
            return jsonify({'imageUrl': image_url, 'qrCodeDataUrl': qr_code_data_url})
        else:
            return jsonify({'error': 'Image processing failed'}), 500
    else:
        return jsonify({'error': 'Background removal failed'}), 500


# Other functions: process_image_with_logo_and_qr, generate_qr_code...

def process_image_with_logo_and_qr(input_path, output_path, background_path, logo_path, qr_data):
    # Load the background image
    background = Image.open(background_path)

    # Load the input (foreground) image
    foreground = Image.open(input_path).convert("RGBA")

    # Resize foreground to match the size of the background image, if necessary
    foreground = foreground.resize(background.size, Image.Resampling.LANCZOS)

    # Paste the foreground onto the background
    background.paste(foreground, (0, 0), foreground)

    # Load the logo
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = (800, 800)  # Adjust size as needed
    logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

    # Paste the logo on the top left corner
    background.paste(logo, (0, 0), logo)

    # Generate and paste the QR code
    qr_code_img = generate_qr_code(qr_data)
    qr_code_size = (800, 800)  # Adjust size as needed
    qr_code_img = qr_code_img.resize(qr_code_size, Image.Resampling.LANCZOS)

    # Calculate position for QR code (top right corner)
    qr_position = (background.size[0] - qr_code_size[0], 0)
    background.paste(qr_code_img, qr_position, qr_code_img)

    # Save the final image
    background.save(output_path)
    return output_path

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill='black', back_color='white')

@app.route('/view-image/<filename>')
def view_image(filename):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>View Image</title>
    </head>
    <body>
        <img src="{url_for('static', filename=f'{output_dir}/' + filename)}" alt="Processed Image" style="max-width: 100%;">
        <br>
        <a href="{url_for('static', filename=f'{output_dir}/' + filename)}" download="{filename}">Download Image</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=False)

