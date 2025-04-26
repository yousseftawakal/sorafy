from PIL import Image, ImageFilter, ImageChops
import numpy as np

def apply_neon_glow(img, params=None):
    params = params or {}
    intensity = params.get('intensity', 5) 
    glow_color = params.get('color', (0, 255, 255))  
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    if isinstance(glow_color, str):
        hex_color = glow_color.lstrip('#')
        glow_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    gray = img.convert('L')
    
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = edges.filter(ImageFilter.SHARPEN)
    edges = edges.point(lambda x: 255 if x > 30 else 0)
    
    glow = edges.filter(ImageFilter.GaussianBlur(radius=intensity))
    
    color_layer = Image.new('RGB', glow.size, glow_color)
    glow = ImageChops.multiply(glow.convert('RGB'), color_layer)
    
    result = ImageChops.screen(img, glow)
    
    return result