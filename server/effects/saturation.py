from PIL import Image, ImageEnhance

def apply_saturation(img, params=None):
    if params is None:
        params = {}

    level = params.get('level', 1.0)

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(level)

    return img


