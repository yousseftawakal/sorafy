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
                {'id': 'factor', 'name': 'Brightness Factor', 'type': 'slider', 'min': 0, 'max': 5, 'step': 0.1, 'default': 1.5}
            ]
        },
        'hue_rotation': {
            'name': 'Hue Rotation',
            'description': 'Rotate the hues of the image',
            'params': [
                {'id': 'angle', 'name': 'Angle', 'type': 'slider', 'min': -180, 'max': 180, 'step': 1, 'default': 45}
            ]
        },
        'sharpen': {
            'name': 'Sharpen',
            'description': 'Apply sharpening effect to the image',
            'params': [
                {'id': 'strength', 'name': 'Strength', 'type': 'slider', 'min': 1, 'max': 20, 'step': 0.1, 'default': 1.5}
            ]
        },
        'edge_detection': {
            'name': 'Edge Detection',
            'description': 'Detects edges in the image',
            'params': [
                {'id': 'threshold', 'name': 'Edge Threshold', 'type': 'slider', 'min': 0, 'max': 255, 'step': 1, 'default': 0}
            ]
        },
        'neon_glow': {
            'name': 'Neon Glow',
            'description': 'Adds a glowing neon effect to edges',
            'params': [ 
                {'id': 'intensity', 'name': 'Glow Intensity', 'type': 'slider', 'min': 3, 'max': 20, 'step': 1, 'default': 8},
                {'id': 'color', 'name': 'Glow Color', 'type': 'color', 'default': '#00FFFF'}
            ]
        },
        'denoise':{
            'name': 'Noise Removal',
            'description': 'Reduces image noise',
            'params': [{ 'id': 'size','name': 'Denoising Size', 'type': 'slider', 'min': 1,'max': 7,'step': 2, 'default': 3}]
        },
        'grayscale': {
            'name': 'Grayscale',
            'description': 'Convert image to grayscale',
            'params': [
                {'id': 'intensity', 'name': 'Grayscale Intensity', 'type': 'slider', 'min': 0, 'max': 1, 'step': 0.1, 'default': 1.0}
            ]
        }
    }
    
    available_effects = {k: v for k, v in effect_info.items() if k in EFFECTS}
    
    return jsonify(available_effects)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
