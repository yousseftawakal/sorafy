from PIL import Image, ImageEnhance

def apply_saturation(img, params=None):
    if params is None:
        params = {}

    factor = float(params.get('factor', 1.0))  

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(factor)

    return img


