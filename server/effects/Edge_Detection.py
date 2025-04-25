from PIL import Image, ImageFilter

def apply_edge_detection(img, params=None):
   
    params = params or {}
    threshold = params.get('threshold', 0)  

    gray_img = img.convert('L')
    edge_img = gray_img.filter(ImageFilter.FIND_EDGES)
    
    if threshold > 0:
        edge_img = edge_img.point(lambda x: 255 if x > threshold else 0)
    
    if img.mode != 'L':
        edge_img = edge_img.convert('RGB')
    
    return edge_img