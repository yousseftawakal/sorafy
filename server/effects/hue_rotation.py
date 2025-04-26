import colorsys
import numpy as np
from PIL import Image

def apply_hue_rotation(img, params=None):
    angle = params.get('angle', 45)
    img = img.convert('RGB')
    np_img = np.array(img) / 255.0
    r, g, b = np_img[..., 0], np_img[..., 1], np_img[..., 2]
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(r, g, b)
    h = (h + angle / 360.0) % 1.0
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(h, s, v)
    np_img = np.stack((r, g, b), axis=-1)
    np_img = (np_img * 255).astype(np.uint8)
    return Image.fromarray(np_img)
