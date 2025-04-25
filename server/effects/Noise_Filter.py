from PIL import Image, ImageFilter

def apply_denoise(img, params=None):
    
    params = params or {}
    strength = params.get('strength', 3) 
    
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGB')
    
    denoised = img.filter(ImageFilter.MedianFilter(size=strength))

    if strength > 3:
        denoised = denoised.filter(ImageFilter.GaussianBlur(radius=min(1, strength/6)))
    
    return denoised