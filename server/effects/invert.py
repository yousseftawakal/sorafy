from PIL import Image, ImageChops, ImageEnhance

def apply_invert(img, params=None):
    if params is None:
        params = {}
        
    intensity = params.get('intensity', 1.0)
    
    inverted = ImageChops.invert(img)
    
    if intensity <= 1:
        result = Image.blend(img, inverted, intensity)
    else:
        result = Image.blend(inverted, img, intensity - 1)
    
    return result

