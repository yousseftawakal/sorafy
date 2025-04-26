from .blur import apply_blur
from .salt_pepper import apply_salt_and_pepper
from .brightness import apply_brightness
from .hue_rotation import apply_hue_rotation
from .sharpen import apply_sharpen
from .denoise import apply_denoise
from .Edge_Detection import apply_edge_detection
from .Neon_Glow import apply_neon_glow
from .grayscale import apply_grayscale
from .saturation import apply_saturation

EFFECTS = {
    'blur': apply_blur,
    'salt_pepper': apply_salt_and_pepper,
    'brightness': apply_brightness,
    'hue_rotation': apply_hue_rotation,
    'sharpen': apply_sharpen,
    'denoise': apply_denoise,
    'edge_detection': apply_edge_detection,
    'neon_glow': apply_neon_glow,
    'grayscale' : apply_grayscale,
    'saturation' : apply_saturation
}

def apply_effect(img, effect_id, params):
    if effect_id in EFFECTS:
        try:
            return EFFECTS[effect_id](img, params)
        except Exception as e:
            print(f"Error applying effect {effect_id}: {str(e)}")
            return img
    else:
        print(f"Effect {effect_id} not found")
        return img
