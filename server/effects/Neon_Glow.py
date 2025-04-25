from PIL import Image, ImageFilter, ImageChops

def apply_neon_glow(img, params=None):
  
    params = params or {}
    intensity = params.get('intensity', 5) 
    glow_color = params.get('color', (0, 255, 255))  
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    edges = img.filter(ImageFilter.FIND_EDGES)
    edges = ImageChops.invert(edges)
   
    glow = edges.filter(ImageFilter.GaussianBlur(radius=intensity))
    
    color_layer = Image.new('RGB', glow.size, glow_color)
    glow = ImageChops.multiply(glow, color_layer)
    
    result = ImageChops.add(img, glow)
    
    return result