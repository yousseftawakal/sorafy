from PIL import Image, ImageEnhance

def apply_grayscale(img, params=None):
    
  if params is None:
        params = {}
        
  intensity = params.get('intensity', 1.0)  # 1.0 means full grayscale, 0.0 means original color
  
  enhancer = ImageEnhance.Color(img)
  img = enhancer.enhance(1.0 - intensity)  # Invert intensity to match slider behavior
   
  
  return img


