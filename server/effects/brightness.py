from PIL import ImageEnhance

def apply_brightness(img, params=None):
    brightness_factor = params.get('factor', 1.5)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(brightness_factor)
