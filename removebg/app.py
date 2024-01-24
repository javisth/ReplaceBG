from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import background_remover  # Adjust this to your background removal logic
import os

app = Flask(__name__)
CORS(app)

output_dir = 'output'
backgrounds_dir = 'berlin'  # Adjust this to your backgrounds directory
os.makedirs(output_dir, exist_ok=True)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    background_filename = request.form.get('background')
    if not background_filename:
        return jsonify({'error': 'No background selected'}), 400

    image = request.files['image']
    input_path = os.path.join(output_dir, 'input_image.jpg')
    output_path = os.path.join(output_dir, 'output_image.png')
    background_path = os.path.join(backgrounds_dir, background_filename)

    image.save(input_path)

    # Assuming your background_remover.process_image function takes the input image path,
    # output image path, and the background image path.
    if background_remover.process_image(input_path, output_path, background_path):
        return send_file(output_path, mimetype='image/png')
    else:
        return jsonify({'error': 'Background removal failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
