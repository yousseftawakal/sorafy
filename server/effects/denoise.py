from PIL import Image, ImageFilter

def apply_denoise(img, params=None):
    
    params = params or {}
    size = params.get('size', 3) 
    
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGB')
    
    denoised = img.filter(ImageFilter.MedianFilter(size=size))

    if size > 3:
        denoised = denoised.filter(ImageFilter.GaussianBlur(radius=min(1, size/6)))
    
    return denoised