from PIL import ImageFilter

def apply_sharpen(img, params=None):
    return img.filter(ImageFilter.SHARPEN)
