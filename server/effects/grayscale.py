from PIL import Image, ImageEnhance

def apply_grayscale(img, params=None):
    
  if params is None:
        params = {}
        
  intensity = params.get('intensity', 1.0)
  
  enhancer = ImageEnhance.Color(img)
  img = enhancer.enhance(1.0 - intensity)
   
  
  return img


