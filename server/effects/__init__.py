from .blur import apply_blur
from .salt_pepper import apply_salt_and_pepper
from .saturation import apply_saturation

EFFECTS = {
    'blur': apply_blur,
    'salt_pepper': apply_salt_and_pepper,
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
