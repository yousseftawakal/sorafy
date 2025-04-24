from PIL import Image
import random

def apply_salt_and_pepper(img, params=None):

    noise_level= params.get('noise_level', 0.02)
    block_size = params.get('block_size', 1)

    pixels = img.load()
    width, height = img.size

    blocks_x = width // block_size
    blocks_y = height // block_size
    noisy_blocks = int(blocks_x * blocks_y * noise_level)

    used_blocks = set()

    for _ in range(noisy_blocks):
        attempts = 0
        while attempts < 100:
            block_x = random.randint(0, blocks_x - 1)
            block_y = random.randint(0, blocks_y - 1)
            
            is_valid = True
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    check_x = block_x + dx
                    check_y = block_y + dy
                    if (check_x, check_y) in used_blocks:
                        is_valid = False
                        break
                if not is_valid:
                    break
            
            if is_valid:
                used_blocks.add((block_x, block_y))
                for x in range(block_x * block_size, min((block_x + 1) * block_size, width)):
                    for y in range(block_y * block_size, min((block_y + 1) * block_size, height)):
                        if random.random() < 0.5:
                            pixels[x, y] = 0
                        else:
                            pixels[x, y] = 255
                break
            
            attempts += 1

    return img
