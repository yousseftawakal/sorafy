from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
import io
from PIL import Image

from effects import apply_effect

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        effects_json = request.form.get('effects', '[]')
        effects = json.loads(effects_json)
        
        img = Image.open(image_file)
        
        for effect in effects:
            effect_id = effect.get('id')
            params = effect.get('params', {})
            
            img = apply_effect(img, effect_id, params)
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({'image': img_str})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/effects', methods=['GET'])
def get_available_effects():
    from effects import EFFECTS
    
    effect_info = {
        'blur': {
            'name': 'Blur',
            'description': 'Apply blur effect',
            'params': [
                {'id': 'radius', 'name': 'Radius', 'type': 'slider', 'min': 0, 'max': 20, 'step': 0.5, 'default': 5}
            ]
        },
        'salt_pepper': {
            'name': 'Salt & Pepper',
            'description': 'Apply salt & pepper effect',
            'params': [
                {'id': 'noise_level', 'name': 'Noise Level', 'type': 'slider', 'min': 0, 'max': 1, 'step': 0.01, 'default': 0.02},
                {'id': 'block_size', 'name': 'Block Size', 'type': 'slider', 'min': 0, 'max': 50, 'step': 1, 'default': 1}
            ]
        },
        'brightness': {
        'name': 'Brightness',
        'description': 'Adjust the brightness of the image',
        'params': [
            {'id': 'factor', 'name': 'Brightness Factor', 'type': 'slider', 'min': 0, 'max': 2, 'step': 0.1, 'default': 1.0}
        ]
    },
    }
    
    available_effects = {k: v for k, v in effect_info.items() if k in EFFECTS}
    
    return jsonify(available_effects)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
