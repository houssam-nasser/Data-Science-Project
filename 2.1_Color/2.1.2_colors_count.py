from PIL import Image
import numpy as np

def count_colors(image_path):
    """
    Efficiently counts the number of unique colors in an image.

    Args:
        image_path: The path to the image file.

    Returns:
        The number of unique colors, or -1 on error.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = np.array(img).reshape(-1, 3)
        return len(np.unique(pixels, axis=0))
    except Exception as e:
        print(f"Error: {e}")  # Log the specific error
        return -1

print(count_colors('Color/2. Count/blue.jpg'))
print(count_colors('Color/2. Count/monochrome_blue.png'))
print(count_colors('Color/original.jpg'))