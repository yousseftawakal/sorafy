from PIL import Image
import numpy as np


def apply_invert(img, params=None):
    img_array = np.array(img)
    
    inverted_array = 255 - img_array
    inverted_img = Image.fromarray(inverted_array)
    return inverted_img

