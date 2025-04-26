from PIL import ImageFilter, ImageEnhance

def apply_sharpen(img, params=None):
    strength = params.get('strength', 1.5)
    
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(strength)
