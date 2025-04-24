from PIL import ImageFilter

def apply_blur(img, params=None):
    radius = params.get('radius', 2) if params else 2
    return img.filter(ImageFilter.GaussianBlur(radius=radius))
