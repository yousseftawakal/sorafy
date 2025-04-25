from PIL import Image, ImageEnhance

def apply_grayscale(img, params=None):
    
  if params is None:
        params = {}
        
  enhancer = ImageEnhance.Color(img)
  img = enhancer.enhance(0) 
   
  
  return img


